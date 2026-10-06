import json
import math
import subprocess
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = PROJECT_ROOT.parent
TOLERANCE = 1e-5


def committed_json(repo_path):
    raw = subprocess.check_output(
        ["git", "show", f"HEAD:{repo_path}"],
        cwd=REPO_ROOT,
        text=True,
    )
    return json.loads(raw)


def generated_json(relative_path):
    return json.loads(
        (PROJECT_ROOT / relative_path).read_text(encoding="utf-8")
    )


def close(name, expected, actual, errors):
    if not math.isclose(
        float(expected),
        float(actual),
        rel_tol=TOLERANCE,
        abs_tol=TOLERANCE,
    ):
        errors.append(
            f"{name} drifted: committed={expected!r}, generated={actual!r}"
        )


def verify_retrieval(errors):
    path = "llm-knowledge-base-assistant/eval/results.json"
    expected = committed_json(path)
    actual = generated_json("eval/results.json")

    for key in ("total_questions", "answerable_questions", "top_k"):
        if expected[key] != actual[key]:
            errors.append(
                f"results.{key} drifted: "
                f"committed={expected[key]!r}, generated={actual[key]!r}"
            )

    for key in ("hit_at_1", "hit_at_3", "mrr_at_3"):
        close(f"results.{key}", expected[key], actual[key], errors)


def verify_calibration(errors):
    path = "llm-knowledge-base-assistant/eval/threshold.json"
    expected = committed_json(path)
    actual = generated_json("eval/threshold.json")

    exact_keys = (
        "schema_version",
        "generated_by",
        "dataset",
        "embedding_model",
        "embedding_revision",
        "optimization_metric",
    )
    for key in exact_keys:
        if expected[key] != actual[key]:
            errors.append(
                f"threshold.{key} drifted: "
                f"committed={expected[key]!r}, generated={actual[key]!r}"
            )

    for key in (
        "threshold",
        "balanced_accuracy",
        "answerable_recall",
        "unanswerable_recall",
    ):
        close(f"threshold.{key}", expected[key], actual[key], errors)

    expected_records = expected["records"]
    actual_records = actual["records"]

    if len(expected_records) != len(actual_records):
        errors.append(
            "threshold.records length drifted: "
            f"committed={len(expected_records)}, generated={len(actual_records)}"
        )
        return

    for index, (left, right) in enumerate(
        zip(expected_records, actual_records),
        start=1,
    ):
        for key in ("id", "question", "answerable"):
            if left[key] != right[key]:
                errors.append(
                    f"threshold.records[{index}].{key} drifted: "
                    f"committed={left[key]!r}, generated={right[key]!r}"
                )

        close(
            f"threshold.records[{index}].top_score",
            left["top_score"],
            right["top_score"],
            errors,
        )


def main():
    errors = []
    verify_retrieval(errors)
    verify_calibration(errors)

    if errors:
        raise SystemExit(
            "RAG evaluation drift exceeded tolerance "
            f"({TOLERANCE:g}):\n"
            + "\n".join(f"- {error}" for error in errors)
        )

    print(
        "RAG evaluation matches the committed snapshot "
        f"within tolerance {TOLERANCE:g}."
    )


if __name__ == "__main__":
    main()
