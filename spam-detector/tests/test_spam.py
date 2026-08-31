import sys
from pathlib import Path

from fastapi.testclient import TestClient


PROJECT_DIR = Path(__file__).parents[1]
sys.path.insert(0, str(PROJECT_DIR))

from app import app, pipeline


client = TestClient(app)


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
