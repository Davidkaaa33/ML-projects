import json
from pathlib import Path

import Levenshtein
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split


RANDOM_STATE = 42
PROJECT_DIR = Path(__file__).parent
DATA_PATH = PROJECT_DIR / "data" / "t9_typo_correction_dataset.csv"
RESULTS_PATH = PROJECT_DIR / "artifacts" / "classifier_results.json"
FEATURE_COLUMNS = [
    "edit_distance",
    "candidate_length",
    "typo_length",
    "length_difference",
    "same_first_letter",
]


def extract_candidate_features(typo_word, candidate_word):
    return {
        "edit_distance": Levenshtein.distance(typo_word, candidate_word),
        "candidate_length": len(candidate_word),
        "typo_length": len(typo_word),
        "length_difference": len(candidate_word) - len(typo_word),
        "same_first_letter": int(typo_word[0] == candidate_word[0]),
    }


def build_features(data):
    return pd.DataFrame(
        [
            extract_candidate_features(row.typo_word, row.correct_word)
            for row in data.itertuples()
        ]
    )[FEATURE_COLUMNS]


def train_and_evaluate():
    data = pd.read_csv(DATA_PATH)
    X = build_features(data)
    y = data["typo_type"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_STATE, stratify=y
    )
    model = RandomForestClassifier(
        n_estimators=200, max_depth=8, random_state=RANDOM_STATE
    )
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    report_text = classification_report(
        y_test,
        predictions,
        zero_division=0,
    )
    report_dict = classification_report(
        y_test,
        predictions,
        zero_division=0,
        output_dict=True,
    )
    return model, accuracy, report_text, report_dict


def predict_typo_type(model, typo_word, selected_candidate):
    features = pd.DataFrame(
        [extract_candidate_features(typo_word, selected_candidate)],
        columns=FEATURE_COLUMNS,
    )
    return model.predict(features)[0]


def main():
    model, accuracy, report, report_dict = train_and_evaluate()
    print(f"Test accuracy: {accuracy:.4f}")
    print(report)

    RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESULTS_PATH.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "generated_by": "typo_type_classifier.py",
                "dataset": {
                    "path": "data/t9_typo_correction_dataset.csv",
                    "synthetic": True,
                },
                "split": {
                    "train": 0.80,
                    "test": 0.20,
                    "stratified": True,
                    "random_state": RANDOM_STATE,
                },
                "evaluation_scope": (
                    "Conditional typo-type classification using the known correct candidate"
                ),
                "accuracy": float(accuracy),
                "classification_report": report_dict,
            },
            indent=2,
            default=float,
        ) + "\n",
        encoding="utf-8",
    )
    print(f"Saved metrics to {RESULTS_PATH}")
    print("Example type:", predict_typo_type(model, "pythom", "python"))


if __name__ == "__main__":
    main()
