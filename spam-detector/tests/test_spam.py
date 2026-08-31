import sys
from pathlib import Path

from fastapi.testclient import TestClient
from sklearn.model_selection import train_test_split


PROJECT_DIR = Path(__file__).parents[1]
sys.path.insert(0, str(PROJECT_DIR))

from app import app, pipeline
from train import RANDOM_STATE, load_data


client = TestClient(app)


def test_train_test_messages_do_not_overlap():
    data = load_data()
    X_train, X_test = train_test_split(
        data["message"],
        test_size=0.2,
        random_state=RANDOM_STATE,
        stratify=data["label"],
    )
    assert set(X_train).isdisjoint(set(X_test))


def test_pipeline_predicts_one_message():
    prediction = pipeline.predict(["Free entry in a weekly prize draw"])
    assert prediction[0] in {"ham", "spam"}


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_prediction_response():
    response = client.post("/predict", json={"text": "Call me when you arrive"})
    body = response.json()
    assert response.status_code == 200
    assert body["label"] in {"ham", "spam"}
    assert 0 <= body["spam_probability"] <= 1
