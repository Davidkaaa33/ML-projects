import sys
from pathlib import Path

import pandas as pd
from sklearn.linear_model import LogisticRegression

PROJECT_DIR = Path(__file__).parents[1]
sys.path.insert(0, str(PROJECT_DIR))

from train import DATA_PATH, build_pipeline, calculate_metrics


def balanced_sample(rows_per_class=80):
    data = pd.read_csv(DATA_PATH)
    sample = (
        data.groupby("is_refunded", group_keys=False)
        .head(rows_per_class)
        .reset_index(drop=True)
    )
    X = sample.drop(columns=["customer_id", "is_refunded"])
    y = sample["is_refunded"]
    return X, y


def test_pipeline_predicts_probabilities():
    X, y = balanced_sample()
    pipeline = build_pipeline(
        LogisticRegression(max_iter=1000, random_state=42),
        scale_numeric=True,
    )
    pipeline.fit(X, y)

    probabilities = pipeline.predict_proba(X.head(5))[:, 1]

    assert probabilities.shape == (5,)
    assert ((0 <= probabilities) & (probabilities <= 1)).all()


def test_pipeline_handles_unseen_category():
    X, y = balanced_sample()
    pipeline = build_pipeline(
        LogisticRegression(max_iter=1000, random_state=42),
        scale_numeric=True,
    )
    pipeline.fit(X, y)

    unseen = X.head(1).copy()
    unseen.loc[:, "employment_status"] = "new_unseen_status"

    probability = pipeline.predict_proba(unseen)[0, 1]

    assert 0 <= probability <= 1


def test_metrics_for_perfect_ranking():
    metrics = calculate_metrics(
        pd.Series([0, 1, 0, 1]),
        pd.Series([0.05, 0.95, 0.10, 0.90]).to_numpy(),
    )

    assert metrics["roc_auc"] == 1.0
    assert metrics["accuracy"] == 1.0
    assert metrics["precision"] == 1.0
    assert metrics["recall"] == 1.0
    assert metrics["f1"] == 1.0
