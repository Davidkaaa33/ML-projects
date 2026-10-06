import json
from pathlib import Path

from app.retrieval import Retriever


EVAL_DIR = Path(__file__).resolve().parent
DATASET_PATH = EVAL_DIR / "questions.json"
RESULTS_PATH = EVAL_DIR / "results.json"
TOP_K = 3


def evaluate():
    dataset = json.loads(
        DATASET_PATH.read_text(encoding="utf-8")
    )

    retriever = Retriever()

    hit_at_1 = 0
    hit_at_3 = 0
    reciprocal_rank_sum = 0.0

    supported = [
        item for item in dataset
        if item["answerable"]
    ]

    for item in supported:
        results = retriever.retrieve(
            query=item["question"],
            top_k=TOP_K,
        )

        retrieved_ids = [
            f"{r['chunk'].source}:{r['chunk'].chunk_id}"
            for r in results
        ]

        relevant = set(item["relevant_chunks"])
        first_relevant_rank = None

        for rank, chunk_id in enumerate(
            retrieved_ids,
            start=1,
        ):
            if chunk_id in relevant:
                first_relevant_rank = rank
                break

        if first_relevant_rank is not None:
            reciprocal_rank_sum += (
                1.0 / first_relevant_rank
            )
            hit_at_3 += 1

            if first_relevant_rank == 1:
                hit_at_1 += 1

        print(f"\nQuestion: {item['question']}")
        print(f"Retrieved: {retrieved_ids}")

        if first_relevant_rank is None:
            print("Result: MISS")
        else:
            print(
                f"Result: HIT "
                f"(rank {first_relevant_rank})"
            )

    n = len(supported)
    metrics = {
        "total_questions": len(dataset),
        "answerable_questions": n,
        "top_k": TOP_K,
        "hit_at_1": hit_at_1 / n,
        "hit_at_3": hit_at_3 / n,
        "mrr_at_3": reciprocal_rank_sum / n,
    }

    RESULTS_PATH.write_text(
        json.dumps(metrics, indent=2) + "\n",
        encoding="utf-8",
    )

    print("\n" + "=" * 50)
    print("RETRIEVAL EVALUATION")
    print("=" * 50)
    print(f"Questions evaluated: {n}")
    print(f"Hit@1: {metrics['hit_at_1']:.2%}")
    print(f"Hit@3: {metrics['hit_at_3']:.2%}")
    print(f"MRR@3: {metrics['mrr_at_3']:.4f}")
    print(f"Saved metrics to {RESULTS_PATH}")

    return metrics


if __name__ == "__main__":
    evaluate()
