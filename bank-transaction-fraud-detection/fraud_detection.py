from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    average_precision_score,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer, OneHotEncoder, StandardScaler


RANDOM_STATE = 42
DATA_PATH = Path(__file__).parent / "data" / "bank_transactions_fraud_dataset.csv"
TIME_ZONES = {
    "Germany": 1,
    "Kazakhstan": 5,
    "Russia": 3,
    "Turkey": 3,
    "UAE": 4,
    "China": 8,
    "Unknown": 0,
}
CATEGORICAL_COLUMNS = [
    "sender_country",
    "recipient_country",
    "risk_segment",
    "transaction_type",
    "device_type",
]
NUMERIC_COLUMNS = [
    "customer_age",
    "account_age_days",
    "account_balance",
    "avg_transaction_amount",
    "transaction_amount",
    "previous_failed_attempts",
    "transactions_last_24h",
    "days_since_last_transaction",
    "transaction_time_hour",
    "sender_local_hour",
    "recipient_local_hour",
    "night_transaction",
]


def engineer_features(data):
    result = data.copy()
    result["transaction_time_hour"] = pd.to_datetime(
        result["time_by_greenwich"]
    ).dt.hour
    result["sender_local_hour"] = (
        result["transaction_time_hour"]
        + result["sender_country"].map(TIME_ZONES).fillna(0)
    ) % 24
    result["recipient_local_hour"] = (
        result["transaction_time_hour"]
        + result["recipient_country"].map(TIME_ZONES).fillna(0)
    ) % 24
    result["night_transaction"] = (
        result["sender_local_hour"].between(0, 6)
        & result["recipient_local_hour"].between(0, 6)
    ).astype(int)
    return result.drop(columns=["transaction_id", "time_by_greenwich"], errors="ignore")


def build_pipeline(model, scale_numeric=False):
    numeric_transformer = StandardScaler() if scale_numeric else "passthrough"
    preprocessing = ColumnTransformer(
        [
            ("numeric", numeric_transformer, NUMERIC_COLUMNS),
            (
                "categorical",
                OneHotEncoder(handle_unknown="ignore"),
                CATEGORICAL_COLUMNS,
            ),
        ]
    )
    return Pipeline(
        [
            ("feature_engineering", FunctionTransformer(engineer_features)),
            ("preprocessing", preprocessing),
            ("model", model),
        ]
    )


def calculate_metrics(y_true, probabilities, threshold=0.5):
    predictions = (probabilities >= threshold).astype(int)
    return {
        "roc_auc": roc_auc_score(y_true, probabilities),
        "pr_auc": average_precision_score(y_true, probabilities),
        "precision": precision_score(y_true, predictions, zero_division=0),
        "recall": recall_score(y_true, predictions, zero_division=0),
        "f1": f1_score(y_true, predictions, zero_division=0),
    }


def choose_threshold(y_validation, probabilities):
    threshold_results = []
    for threshold in np.arange(0.05, 0.96, 0.05):
        metrics = calculate_metrics(y_validation, probabilities, threshold)
        threshold_results.append((metrics["f1"], threshold))
    return max(threshold_results, key=lambda item: (item[0], -item[1]))[1]


def evaluate_candidates(name, candidates, X_train, y_train, X_validation, y_validation):
    results = []
    for description, pipeline in candidates:
        pipeline.fit(X_train, y_train)
        probabilities = pipeline.predict_proba(X_validation)[:, 1]
        metrics = calculate_metrics(y_validation, probabilities)
        results.append(
            {
                "model": name,
                "configuration": description,
                "pipeline": pipeline,
                **metrics,
            }
        )
    return max(results, key=lambda result: result["pr_auc"])


def predict_transaction(pipeline, threshold, transaction):
    probabilities = pipeline.predict_proba(pd.DataFrame([transaction]))[:, 1]
    probability = float(probabilities[0])
    return {"fraud_probability": probability, "is_fraud": int(probability >= threshold)}


def run_training():
    data = pd.read_csv(DATA_PATH)
    X = data.drop(columns="is_fraud")
    y = data["is_fraud"]

    X_train_validation, X_test, y_train_validation, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_STATE, stratify=y
    )
    X_train, X_validation, y_train, y_validation = train_test_split(
        X_train_validation,
        y_train_validation,
        test_size=0.25,
        random_state=RANDOM_STATE,
        stratify=y_train_validation,
    )

    baseline = build_pipeline(DummyClassifier(strategy="prior"))
    logistic_candidates = [
        (
            f"C={c}, class_weight={class_weight}",
            build_pipeline(
                LogisticRegression(
                    C=c,
                    class_weight=class_weight,
                    max_iter=1000,
                    random_state=RANDOM_STATE,
                ),
                scale_numeric=True,
            ),
        )
        for c in [0.1, 1.0]
        for class_weight in [None, "balanced"]
    ]
    forest_candidates = [
        (
            f"max_depth={max_depth}, min_samples_leaf={min_samples_leaf}, "
            f"class_weight={class_weight}",
            build_pipeline(
                RandomForestClassifier(
                    n_estimators=200,
                    max_depth=max_depth,
                    min_samples_leaf=min_samples_leaf,
                    class_weight=class_weight,
                    random_state=RANDOM_STATE,
                    n_jobs=-1,
                )
            ),
        )
        for max_depth in [8, None]
        for min_samples_leaf in [1, 4]
        for class_weight in [None, "balanced"]
    ]

    comparison = [
        evaluate_candidates(
            "Dummy baseline",
            [("class prior", baseline)],
            X_train,
            y_train,
            X_validation,
            y_validation,
        ),
        evaluate_candidates(
            "Logistic Regression",
            logistic_candidates,
            X_train,
            y_train,
            X_validation,
            y_validation,
        ),
        evaluate_candidates(
            "Random Forest",
            forest_candidates,
            X_train,
            y_train,
            X_validation,
            y_validation,
        ),
    ]

    comparison_table = pd.DataFrame(comparison).drop(columns="pipeline")
    best_result = max(comparison[1:], key=lambda result: result["pr_auc"])
    best_pipeline = best_result["pipeline"]
    validation_probabilities = best_pipeline.predict_proba(X_validation)[:, 1]
    threshold = choose_threshold(y_validation, validation_probabilities)

    test_probabilities = best_pipeline.predict_proba(X_test)[:, 1]
    test_metrics = calculate_metrics(y_test, test_probabilities, threshold)
    return comparison_table, best_result, threshold, test_metrics, best_pipeline


def main():
    comparison, best_result, threshold, test_metrics, pipeline = run_training()
    print("Validation comparison (best configuration per model):")
    print(comparison.to_string(index=False, float_format=lambda value: f"{value:.4f}"))
    print(f"\nFinal model: {best_result['model']} ({best_result['configuration']})")
    print(f"Chosen validation threshold: {threshold:.2f}")
    print("Final untouched test metrics:")
    for metric, value in test_metrics.items():
        print(f"{metric}: {value:.4f}")

    example = {
        "customer_age": 62,
        "account_age_days": 300,
        "account_balance": 12000,
        "avg_transaction_amount": 500,
        "transaction_amount": 4500,
        "previous_failed_attempts": 3,
        "transactions_last_24h": 8,
        "days_since_last_transaction": 1,
        "time_by_greenwich": "2026-01-01 02:00:00",
        "sender_country": "Russia",
        "recipient_country": "UAE",
        "risk_segment": "high",
        "transaction_type": "online_transfer",
        "device_type": "desktop",
    }
    print("\nExample inference:", predict_transaction(pipeline, threshold, example))


if __name__ == "__main__":
    main()
