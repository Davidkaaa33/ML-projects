from pathlib import Path

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


RANDOM_STATE = 42
DATA_PATH = Path(__file__).parent / "data" / "credit_repayment_dataset.csv"
CATEGORICAL_COLUMNS = ["employment_status", "loan_purpose", "payment_method"]
NUMERIC_COLUMNS = [
    "credit_amount",
    "customer_age",
    "credit_score",
    "income",
    "previous_loans",
    "previous_refunds",
    "late_payments",
    "days_since_credit",
    "support_tickets",
]


def build_pipeline(model, scale_numeric=False):
    preprocessing = ColumnTransformer(
        [
            (
                "numeric",
                StandardScaler() if scale_numeric else "passthrough",
                NUMERIC_COLUMNS,
            ),
            (
                "categorical",
                OneHotEncoder(handle_unknown="ignore"),
                CATEGORICAL_COLUMNS,
            ),
        ]
    )
    return Pipeline([("preprocessing", preprocessing), ("model", model)])


def calculate_metrics(y_true, probabilities):
    predictions = (probabilities >= 0.5).astype(int)
    return {
        "roc_auc": roc_auc_score(y_true, probabilities),
        "accuracy": accuracy_score(y_true, predictions),
        "precision": precision_score(y_true, predictions, zero_division=0),
        "recall": recall_score(y_true, predictions, zero_division=0),
        "f1": f1_score(y_true, predictions, zero_division=0),
    }


def choose_best(name, candidates, X_train, y_train, X_validation, y_validation):
    results = []
    for description, pipeline in candidates:
        pipeline.fit(X_train, y_train)
        probabilities = pipeline.predict_proba(X_validation)[:, 1]
        results.append(
            {
                "model": name,
                "configuration": description,
                "pipeline": pipeline,
                **calculate_metrics(y_validation, probabilities),
            }
        )
    return max(results, key=lambda result: result["roc_auc"])


def random_forest_feature_importance(pipeline):
    feature_names = pipeline.named_steps["preprocessing"].get_feature_names_out()
    importance = pipeline.named_steps["model"].feature_importances_
    return (
        pd.DataFrame({"feature": feature_names, "importance": importance})
        .sort_values("importance", ascending=False)
        .head(10)
    )


def run_training():
    data = pd.read_csv(DATA_PATH)
    X = data.drop(columns=["customer_id", "is_refunded"])
    y = data["is_refunded"]

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

    logistic_candidates = [
        (
            f"C={c}",
            build_pipeline(
                LogisticRegression(C=c, max_iter=1000, random_state=RANDOM_STATE),
                scale_numeric=True,
            ),
        )
        for c in [0.1, 1.0]
    ]
    forest_candidates = [
        (
            f"max_depth={max_depth}, min_samples_leaf={min_samples_leaf}",
            build_pipeline(
                RandomForestClassifier(
                    n_estimators=200,
                    max_depth=max_depth,
                    min_samples_leaf=min_samples_leaf,
                    random_state=RANDOM_STATE,
                    n_jobs=-1,
                )
            ),
        )
        for max_depth in [6, 10, None]
        for min_samples_leaf in [1, 4]
    ]

    logistic_result = choose_best(
        "Logistic Regression",
        logistic_candidates,
        X_train,
        y_train,
        X_validation,
        y_validation,
    )
    forest_result = choose_best(
        "Random Forest",
        forest_candidates,
        X_train,
        y_train,
        X_validation,
        y_validation,
    )
    comparison = [logistic_result, forest_result]
    best_result = max(comparison, key=lambda result: result["roc_auc"])

    test_probabilities = best_result["pipeline"].predict_proba(X_test)[:, 1]
    test_metrics = calculate_metrics(y_test, test_probabilities)
    importance = random_forest_feature_importance(forest_result["pipeline"])
    comparison_table = pd.DataFrame(comparison).drop(columns="pipeline")
    return comparison_table, best_result, test_metrics, importance


def main():
    comparison, best_result, test_metrics, importance = run_training()
    print("Validation comparison (best configuration per model):")
    print(comparison.to_string(index=False, float_format=lambda value: f"{value:.4f}"))
    print(f"\nFinal model: {best_result['model']} ({best_result['configuration']})")
    print("Final untouched test metrics:")
    for metric, value in test_metrics.items():
        print(f"{metric}: {value:.4f}")
    print("\nTop Random Forest feature importances:")
    print(importance.to_string(index=False, float_format=lambda value: f"{value:.4f}"))


if __name__ == "__main__":
    main()
