
import json
import re
from pathlib import Path


EVAL_DIR = Path(__file__).resolve().parent

dataset = json.loads(
    (EVAL_DIR / "questions.json").read_text(
        encoding="utf-8"
    )
)

report = json.loads(
    (EVAL_DIR / "results" / "answer_eval.json").read_text(
        encoding="utf-8"
    )
)

gold = {
    item["id"]: item
    for item in dataset
}

flagged = 0

for result in report["results"]:
    if not result["answerable"]:
        continue

    question_id = result["id"]
    relevant = set(
        gold[question_id]["relevant_chunks"]
    )

    sources = result["retrieved_sources"]

    cited_ranks = [
        int(x)
        for x in re.findall(
            r"\[(\d+)\]",
            result["generated_answer"],
        )
    ]

    problems = []

    if not cited_ranks:
        problems.append("No citations")

    for rank in cited_ranks:
        if not 1 <= rank <= len(sources):
            problems.append(
                f"Invalid citation [{rank}]"
            )
            continue

        source = sources[rank - 1]

        chunk_id = (
            f"{source['source']}:"
            f"{source['chunk_id']}"
        )

        if chunk_id not in relevant:
            problems.append(
                f"[{rank}] {chunk_id} "
                "is not in the reference labels"
            )

    if problems:
        flagged += 1

        print("\n" + "=" * 60)
        print(f"Question {question_id}")
        print(result["question"])
        print("\nAnswer:")
        print(result["generated_answer"])

        print("\nIssues to review:")
        for problem in problems:
            print("-", problem)

print("\n" + "=" * 60)
print(f"Questions flagged for review: {flagged}")
