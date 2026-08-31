from pathlib import Path

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import confusion_matrix, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline


RANDOM_STATE = 42
PROJECT_DIR = Path(__file__).parent
DATA_PATH = PROJECT_DIR / "data" / "spam.csv"
MODEL_PATH = PROJECT_DIR / "model.joblib"


def load_data():
    data = pd.read_csv(DATA_PATH, encoding="latin-1", usecols=["v1", "v2"])
    return data.rename(columns={"v1": "label", "v2": "message"})


def build_pipeline():
    return Pipeline(
        [
            ("tfidf", TfidfVectorizer()),
            ("classifier", MultinomialNB()),
        ]
    )


def evaluate_errors(X_test, y_test, predictions):
    results = pd.DataFrame(
        {"message": X_test.to_numpy(), "actual": y_test.to_numpy(), "predicted": predictions}
    )
    false_positives = results[
        (results["actual"] == "ham") & (results["predicted"] == "spam")
    ]
    false_negatives = results[
        (results["actual"] == "spam") & (results["predicted"] == "ham")
    ]
    return false_positives, false_negatives


def train_and_evaluate():
    data = load_data()
    X_train, X_test, y_train, y_test = train_test_split(
        data["message"],
        data["label"],
        test_size=0.2,
        random_state=RANDOM_STATE,
        stratify=data["label"],
    )

    pipeline = build_pipeline()
    pipeline.fit(X_train, y_train)
    predictions = pipeline.predict(X_test)
    metrics = {
        "precision": precision_score(y_test, predictions, pos_label="spam"),
        "recall": recall_score(y_test, predictions, pos_label="spam"),
        "f1": f1_score(y_test, predictions, pos_label="spam"),
    }
    matrix = confusion_matrix(y_test, predictions, labels=["ham", "spam"])
    false_positives, false_negatives = evaluate_errors(X_test, y_test, predictions)
    return pipeline, metrics, matrix, false_positives, false_negatives


def main():
    pipeline, metrics, matrix, false_positives, false_negatives = train_and_evaluate()
    joblib.dump(pipeline, MODEL_PATH)

    print("Test metrics:")
    for metric, value in metrics.items():
        print(f"{metric}: {value:.4f}")
    print("Confusion matrix (rows: ham/spam, columns: ham/spam):")
    print(matrix)
    print(f"False positives: {len(false_positives)}")
    print(false_positives[["message"]].head(5).to_string(index=False))
    print(f"False negatives: {len(false_negatives)}")
    print(false_negatives[["message"]].head(5).to_string(index=False))
    print(f"Saved pipeline to {MODEL_PATH}")


if __name__ == "__main__":
    main()
