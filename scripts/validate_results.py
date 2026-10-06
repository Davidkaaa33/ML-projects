import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_json(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def unit_interval(name, value, errors):
    if not isinstance(value, (int, float)) or not math.isfinite(value):
        errors.append(f"{name} is not a finite number: {value!r}")
        return
    if not 0 <= value <= 1:
        errors.append(f"{name} must be between 0 and 1: {value}")


def main():
    errors = []

    fraud = load_json("bank-transaction-fraud-detection/artifacts/results.json")
    credit = load_json("credit-repayment-prediction/artifacts/results.json")
    spam = load_json("spam-detector/artifacts/results.json")
    t9_rank = load_json("T9-typo-correction/artifacts/candidate_results.json")
    t9_class = load_json("T9-typo-correction/artifacts/classifier_results.json")
    rag = load_json("llm-knowledge-base-assistant/eval/results.json")

    artifacts = {
        "fraud": fraud,
        "credit": credit,
        "spam": spam,
        "t9_rank": t9_rank,
        "t9_class": t9_class,
        "rag": rag,
    }

    for name, artifact in artifacts.items():
        if artifact.get("schema_version", 1) != 1:
            errors.append(f"{name}: unsupported schema_version")

    for metric, value in fraud["test_metrics"].items():
        unit_interval(f"fraud.{metric}", value, errors)

    for metric, value in credit["test_metrics"].items():
        unit_interval(f"credit.{metric}", value, errors)

    for metric, value in spam["test_metrics"].items():
        unit_interval(f"spam.{metric}", value, errors)

    for metric, value in t9_rank["metrics"].items():
        unit_interval(f"t9_rank.{metric}", value, errors)

    unit_interval("t9_class.accuracy", t9_class["accuracy"], errors)
    unit_interval("rag.hit_at_1", rag["hit_at_1"], errors)
    unit_interval("rag.hit_at_3", rag["hit_at_3"], errors)
    unit_interval("rag.mrr_at_3", rag["mrr_at_3"], errors)

    matrix = spam["confusion_matrix"]["values"]
    if len(matrix) != 2 or any(len(row) != 2 for row in matrix):
        errors.append("spam confusion matrix must be 2x2")
    if any(value < 0 for row in matrix for value in row):
        errors.append("spam confusion matrix cannot contain negative counts")

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    expected_fragments = [
        ("fraud ROC-AUC", f'ROC-AUC **{fraud["test_metrics"]["roc_auc"]:.4f}**'),
        ("fraud PR-AUC", f'PR-AUC **{fraud["test_metrics"]["pr_auc"]:.4f}**'),
        ("credit ROC-AUC", f'ROC-AUC **{credit["test_metrics"]["roc_auc"]:.4f}**'),
        ("credit F1", f'F1 **{credit["test_metrics"]["f1"]:.4f}**'),
        ("spam precision", f'Precision **{spam["test_metrics"]["precision"]:.4f}**'),
        ("spam F1", f'F1 **{spam["test_metrics"]["f1"]:.4f}**'),
        ("T9 Top-1", f'Top-1 **{t9_rank["metrics"]["top_1_accuracy"]:.4f}**'),
        ("T9 Top-3", f'Top-3 **{t9_rank["metrics"]["top_3_recall"]:.4f}**'),
        ("RAG Hit@1", f'Hit@1 **{rag["hit_at_1"]:.2%}**'),
        ("RAG Hit@3", f'Hit@3 **{rag["hit_at_3"]:.0%}**'),
        ("RAG MRR@3", f'MRR@3 **{rag["mrr_at_3"]:.4f}**'),
    ]

    for name, fragment in expected_fragments:
        if fragment not in readme:
            errors.append(f"README is out of sync with {name}: expected {fragment!r}")

    if errors:
        raise SystemExit("\n".join(f"- {error}" for error in errors))

    print("Evaluation artifacts and README headline metrics are consistent.")


if __name__ == "__main__":
    main()
