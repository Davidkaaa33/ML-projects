
import argparse
import json
import re
import time
from pathlib import Path

from app.rag import RAGAssistant


EVAL_DIR = Path(__file__).resolve().parent
DATASET_PATH = EVAL_DIR / "questions.json"
RESULTS_PATH = EVAL_DIR / "results" / "answer_eval.json"

ABSTENTION = "i don't know based on the provided documents"

# Simple factual checks for our 11 answerable questions.
# Every pattern in a question's list must match.
EXPECTED_PATTERNS = {
    1: [r"\b28\b", r"\bdays?\b"],
    2: [r"\b(3|three)\b", r"\bdays?\b"],
    3: [r"\b(2|two)\s+weeks?\b"],
    4: [r"\blaptops?\b"],
    5: [r"\bknowledgeai\b"],
    6: [
        r"\b(internal|company)\b",
        r"\b(documents|documentation)\b",
    ],
    7: [r"\b(rag|retrieval.augmented.generation)\b"],
    8: [r"\bweb\b", r"\binterface\b"],
    9: [
        r"\b(09:00|9:00|9\s*a\.?m\.?)",
        r"\b(18:00|6:00|6\s*p\.?m\.?)",
        r"\bbusiness days\b",
    ],
    10: [r"\bsupport portal\b"],
    11: [
        r"\brequest\b",
        r"\berror\b",
        r"\b(time|timestamp)\b",
    ],
}


def check_facts(question_id, answer):
    patterns = EXPECTED_PATTERNS[question_id]

    return all(
        re.search(pattern, answer, re.IGNORECASE)
        for pattern in patterns
    )


def check_citations(answer, sources, relevant_chunks):
    cited_ranks = [
        int(number)
        for number in re.findall(r"\[(\d+)\]", answer)
    ]

    valid_ranks = [
        rank
        for rank in cited_ranks
        if 1 <= rank <= len(sources)
    ]

    cited_chunks = [
        f"{sources[rank - 1]['source']}:"
        f"{sources[rank - 1]['chunk_id']}"
        for rank in valid_ranks
    ]

    valid_references = (
        bool(cited_ranks)
        and len(valid_ranks) == len(cited_ranks)
    )

    relevant_citation = (
        valid_references
        and any(
            chunk in relevant_chunks
            for chunk in cited_chunks
        )
    )

    return {
        "cited_ranks": cited_ranks,
        "cited_chunks": cited_chunks,
        "valid_references": valid_references,
        "relevant_citation": relevant_citation,
    }


def evaluate(selected_ids=None):
    dataset = json.loads(
        DATASET_PATH.read_text(encoding="utf-8")
    )

    if selected_ids:
        dataset = [
            item
            for item in dataset
            if item["id"] in selected_ids
        ]

    if not dataset:
        raise ValueError("No evaluation questions selected.")

    # Load embeddings and FAISS once, not for each question.
    assistant = RAGAssistant()

    results = []

    for item in dataset:
        print(f"\nEvaluating question {item['id']}...")
        print(item["question"])

        start = time.perf_counter()

        response = assistant.ask(
            question=item["question"],
            top_k=3,
        )

        latency = time.perf_counter() - start
        answer = response["answer"]

        abstained = response.get(
            "abstained",
            ABSTENTION in answer.lower(),
        )

        if item["answerable"]:
            fact_match = (
                not abstained
                and check_facts(item["id"], answer)
            )

            citations = check_citations(
                answer,
                response["retrieved_sources"],
                item["relevant_chunks"],
            )
        else:
            fact_match = None

            citations = {
                "cited_ranks": [],
                "cited_chunks": [],
                "valid_references": None,
                "relevant_citation": None,
            }

        record = {
            "id": item["id"],
            "question": item["question"],
            "answerable": item["answerable"],
            "expected_answer": item["expected_answer"],
            "generated_answer": answer,
            "fact_match": fact_match,
            "abstained": abstained,
            "abstention_reason": response.get("abstention_reason"),
            "top_retrieval_score": response.get("top_retrieval_score"),
            "citations": citations,
            "latency_seconds": round(latency, 2),
            "retrieved_sources": response[
                "retrieved_sources"
            ],
        }

        results.append(record)

        print(f"\nANSWER:\n{answer}")

        if item["answerable"]:
            print(f"Expected facts matched: {fact_match}")
            print(
                "Relevant citation:",
                citations["relevant_citation"],
            )
        else:
            print(f"Correct abstention: {abstained}")

        print(f"Latency: {latency:.2f}s")

    supported = [
        item
        for item in results
        if item["answerable"]
    ]

    unsupported = [
        item
        for item in results
        if not item["answerable"]
    ]

    summary = {
        "total_questions": len(results),
        "answerable_questions": len(supported),
        "unanswerable_questions": len(unsupported),
        "fact_matches": sum(
            item["fact_match"]
            for item in supported
        ),
        "correct_abstentions": sum(
            item["abstained"]
            for item in unsupported
        ),
        "relevant_citations": sum(
            item["citations"]["relevant_citation"]
            for item in supported
        ),
        "average_latency_seconds": round(
            sum(
                item["latency_seconds"]
                for item in results
            ) / len(results),
            2,
        ),
    }

    RESULTS_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    RESULTS_PATH.write_text(
        json.dumps(
            {
                "summary": summary,
                "results": results,
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    print("\n" + "=" * 50)
    print("ANSWER EVALUATION")
    print("=" * 50)

    print(
        f"Expected fact matches: "
        f"{summary['fact_matches']}/{len(supported)}"
    )

    print(
        f"Correct abstentions: "
        f"{summary['correct_abstentions']}/{len(unsupported)}"
    )

    print(
        f"Relevant citations: "
        f"{summary['relevant_citations']}/{len(supported)}"
    )

    print(
        f"Average latency: "
        f"{summary['average_latency_seconds']}s"
    )

    print(f"\nResults saved to: {RESULTS_PATH}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--ids",
        type=int,
        nargs="+",
    )

    args = parser.parse_args()

    evaluate(selected_ids=args.ids)
