import os


THRESHOLD_ENV = "RAG_MIN_RETRIEVAL_SCORE"


def parse_threshold(value: str | None) -> float | None:
    if value is None or not value.strip():
        return None

    threshold = float(value)
    if not -1.0 <= threshold <= 1.0:
        raise ValueError(
            f"{THRESHOLD_ENV} must be between -1.0 and 1.0 for cosine similarity."
        )
    return threshold


def threshold_from_env() -> float | None:
    return parse_threshold(os.getenv(THRESHOLD_ENV))


def evaluate_threshold(records: list[dict], threshold: float) -> dict:
    answerable = [record for record in records if record["answerable"]]
    unanswerable = [record for record in records if not record["answerable"]]

    if not answerable or not unanswerable:
        raise ValueError("Calibration requires both answerable and unanswerable examples.")

    true_positive = sum(
        record["top_score"] >= threshold
        for record in answerable
    )
    true_negative = sum(
        record["top_score"] < threshold
        for record in unanswerable
    )

    answerable_recall = true_positive / len(answerable)
    unanswerable_recall = true_negative / len(unanswerable)
    balanced_accuracy = (answerable_recall + unanswerable_recall) / 2

    return {
        "threshold": float(threshold),
        "balanced_accuracy": balanced_accuracy,
        "answerable_recall": answerable_recall,
        "unanswerable_recall": unanswerable_recall,
    }


def select_threshold(records: list[dict]) -> dict:
    if not records:
        raise ValueError("No calibration records supplied.")

    scores = sorted({float(record["top_score"]) for record in records})
    if not scores:
        raise ValueError("Calibration records have no scores.")

    epsilon = 1e-6
    candidates = [scores[0] - epsilon]
    candidates.extend(
        (left + right) / 2
        for left, right in zip(scores, scores[1:])
    )
    candidates.append(scores[-1] + epsilon)

    evaluated = [
        evaluate_threshold(records, threshold)
        for threshold in candidates
    ]

    return max(
        evaluated,
        key=lambda item: (
            item["balanced_accuracy"],
            item["answerable_recall"],
            item["unanswerable_recall"],
            item["threshold"],
        ),
    )
