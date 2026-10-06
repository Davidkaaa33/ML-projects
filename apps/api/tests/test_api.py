from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_model_registry_has_all_systems():
    response = client.get("/api/models")
    assert response.status_code == 200
    assert {model["id"] for model in response.json()} == {
        "fraud",
        "credit",
        "spam",
        "typo",
        "rag",
    }


def test_spam_prediction_contract():
    response = client.post(
        "/api/spam/predict",
        json={"text": "Free entry in a weekly prize draw"},
    )
    body = response.json()

    assert response.status_code == 200
    assert body["label"] in {"ham", "spam"}
    assert 0 <= body["spam_probability"] <= 1


def test_typo_correction_contract():
    response = client.post(
        "/api/t9/correct",
        json={"text": "I am lerning pythom"},
    )
    body = response.json()

    assert response.status_code == 200
    assert body["corrected"] == "I am learning python"
    assert len(body["corrections"]) == 2


def test_rag_evaluation_is_available_without_ollama():
    response = client.get("/api/rag/evaluation")
    body = response.json()

    assert response.status_code == 200
    assert body["retrieval"]["hit_at_3"] == 1.0
    assert body["abstention"]["threshold"] > 0
