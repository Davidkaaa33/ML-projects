from pathlib import Path

import Levenshtein
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split


RANDOM_STATE = 42
DATA_PATH = Path(__file__).parent / "data" / "t9_typo_correction_dataset.csv"
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
    return model, accuracy_score(y_test, predictions), classification_report(
        y_test, predictions, zero_division=0
    )


def predict_typo_type(model, typo_word, selected_candidate):
    features = pd.DataFrame(
        [extract_candidate_features(typo_word, selected_candidate)],
        columns=FEATURE_COLUMNS,
    )
    return model.predict(features)[0]


def main():
    model, accuracy, report = train_and_evaluate()
    print(f"Test accuracy: {accuracy:.4f}")
    print(report)
    print("Example type:", predict_typo_type(model, "pythom", "python"))


if __name__ == "__main__":
    main()
