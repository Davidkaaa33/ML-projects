import json
from pathlib import Path

from app.confidence import select_threshold
from app.embeddings import MODEL_NAME, MODEL_REVISION
from app.retrieval import Retriever


EVAL_DIR = Path(__file__).resolve().parent
DATASET_PATH = EVAL_DIR / "questions.json"
RESULTS_PATH = EVAL_DIR / "threshold.json"


def calibrate():
    dataset = json.loads(
        DATASET_PATH.read_text(encoding="utf-8")
    )
    retriever = Retriever()

    records = []
    for item in dataset:
        results = retriever.retrieve(
            query=item["question"],
            top_k=1,
        )
        top_score = (
            float(results[0]["score"])
            if results
            else -1.0
        )
        records.append(
            {
                "id": item["id"],
                "question": item["question"],
                "answerable": item["answerable"],
                "top_score": top_score,
            }
        )

    selected = select_threshold(records)

    payload = {
        "schema_version": 1,
        "generated_by": "eval/calibrate_abstention.py",
        "dataset": "eval/questions.json",
        "embedding_model": MODEL_NAME,
        "embedding_revision": MODEL_REVISION,
        "optimization_metric": "balanced_accuracy",
        **selected,
        "records": records,
    }

    RESULTS_PATH.write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8",
    )

    print("ABSTENTION CALIBRATION")
    print("=" * 50)
    print(f"Threshold: {selected['threshold']:.6f}")
    print(
        "Balanced accuracy: "
        f"{selected['balanced_accuracy']:.2%}"
    )
    print(
        "Answerable recall: "
        f"{selected['answerable_recall']:.2%}"
    )
    print(
        "Unanswerable recall: "
        f"{selected['unanswerable_recall']:.2%}"
    )
    print(f"Saved calibration to {RESULTS_PATH}")
    print(
        "Runtime override: "
        f'export RAG_MIN_RETRIEVAL_SCORE="{selected["threshold"]:.6f}"'
    )

    return payload


if __name__ == "__main__":
    calibrate()
