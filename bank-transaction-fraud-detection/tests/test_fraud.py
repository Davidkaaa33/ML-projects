import sys
from pathlib import Path

import pandas as pd
from sklearn.linear_model import LogisticRegression


PROJECT_DIR = Path(__file__).parents[1]
sys.path.insert(0, str(PROJECT_DIR))

from fraud_detection import DATA_PATH, build_pipeline, engineer_features, predict_transaction


def test_feature_engineering_adds_expected_columns():
    raw = pd.read_csv(DATA_PATH, nrows=1).drop(columns="is_fraud")
    engineered = engineer_features(raw)
    expected = {
        "transaction_time_hour",
        "sender_local_hour",
        "recipient_local_hour",
        "night_transaction",
    }
    assert expected.issubset(engineered.columns)


def test_inference_accepts_one_transaction():
    data = pd.read_csv(DATA_PATH)
    training_data = pd.concat(
        [data[data["is_fraud"] == 0].head(100), data[data["is_fraud"] == 1].head(100)]
    )
    X_train = training_data.drop(columns="is_fraud")
    y_train = training_data["is_fraud"]
    pipeline = build_pipeline(
        LogisticRegression(max_iter=1000, random_state=42), scale_numeric=True
    )
    pipeline.fit(X_train, y_train)
    transaction = X_train.iloc[0].to_dict()
    result = predict_transaction(pipeline, 0.5, transaction)
    assert set(result) == {"fraud_probability", "is_fraud"}
    assert 0 <= result["fraud_probability"] <= 1
