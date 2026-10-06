import importlib.util
import json
import os
from functools import lru_cache
from pathlib import Path
from typing import Any

import httpx
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier


ROOT = Path(__file__).resolve().parents[3]


def read_json(relative_path: str) -> dict:
    return json.loads((ROOT / relative_path).read_text(encoding="utf-8"))


@lru_cache
def load_module(relative_path: str, module_name: str):
    path = ROOT / relative_path
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load {relative_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def metric_percent(value: float) -> float:
    return round(float(value) * 100, 2)


def model_registry() -> list[dict[str, Any]]:
    fraud = read_json("bank-transaction-fraud-detection/artifacts/results.json")
    credit = read_json("credit-repayment-prediction/artifacts/results.json")
    spam = read_json("spam-detector/artifacts/results.json")
    typo = read_json("T9-typo-correction/artifacts/candidate_results.json")
    rag = read_json("llm-knowledge-base-assistant/eval/results.json")

    return [
        {
            "id": "fraud",
            "name": "Transaction Risk",
            "task": "Imbalanced classification",
            "description": "Risk scoring for synthetic bank transactions with validation-selected thresholding.",
            "technology": ["Random Forest", "feature engineering", "threshold tuning"],
            "headline_metric": "ROC-AUC",
            "headline_value": f"{fraud['test_metrics']['roc_auc']:.4f}",
            "secondary_metric": f"PR-AUC {fraud['test_metrics']['pr_auc']:.4f}",
            "live": True,
            "data_scope": "Synthetic",
            "repo_path": "bank-transaction-fraud-detection",
        },
        {
            "id": "credit",
            "name": "Credit Repayment",
            "task": "Tabular risk modeling",
            "description": "Repayment probability with leakage-safe preprocessing and held-out evaluation.",
            "technology": ["sklearn Pipeline", "Random Forest", "validation split"],
            "headline_metric": "ROC-AUC",
            "headline_value": f"{credit['test_metrics']['roc_auc']:.4f}",
            "secondary_metric": f"F1 {credit['test_metrics']['f1']:.4f}",
            "live": True,
            "data_scope": "Synthetic",
            "repo_path": "credit-repayment-prediction",
        },
        {
            "id": "spam",
            "name": "SMS Spam",
            "task": "Text classification",
            "description": "Deduplicated SMS classification exposed through a typed inference API.",
            "technology": ["TF-IDF", "Multinomial NB", "FastAPI"],
            "headline_metric": "Precision",
            "headline_value": f"{spam['test_metrics']['precision']:.4f}",
            "secondary_metric": f"F1 {spam['test_metrics']['f1']:.4f}",
            "live": True,
            "data_scope": "SMS Spam Collection",
            "repo_path": "spam-detector",
        },
        {
            "id": "typo",
            "name": "Typo Correction",
            "task": "Candidate generation + ranking",
            "description": "Edit-distance candidate retrieval with deterministic ranking and correction.",
            "technology": ["Levenshtein", "ranking", "closed vocabulary"],
            "headline_metric": "Top-1",
            "headline_value": f"{typo['metrics']['top_1_accuracy']:.4f}",
            "secondary_metric": f"Top-3 {typo['metrics']['top_3_recall']:.4f}",
            "live": True,
            "data_scope": "Synthetic",
            "repo_path": "T9-typo-correction",
        },
        {
            "id": "rag",
            "name": "Knowledge Assistant",
            "task": "Local retrieval-augmented generation",
            "description": "FAISS retrieval, citations and calibrated abstention with optional local Qwen generation.",
            "technology": ["SentenceTransformers", "FAISS", "Qwen / Ollama"],
            "headline_metric": "Hit@1",
            "headline_value": f"{metric_percent(rag['hit_at_1']):.2f}%",
            "secondary_metric": f"MRR@3 {rag['mrr_at_3']:.4f}",
            "live": bool(os.getenv("RAG_SERVICE_URL")),
            "data_scope": "Included document corpus",
            "repo_path": "llm-knowledge-base-assistant",
        },
    ]


@lru_cache
def spam_pipeline():
    return joblib.load(ROOT / "spam-detector" / "model.joblib")


def predict_spam(text: str) -> dict[str, Any]:
    pipeline = spam_pipeline()
    probabilities = pipeline.predict_proba([text])[0]
    spam_index = list(pipeline.classes_).index("spam")
    probability = float(probabilities[spam_index])
    label = str(pipeline.predict([text])[0])
    return {
        "label": label,
        "spam_probability": probability,
        "confidence": probability if label == "spam" else 1 - probability,
    }


@lru_cache
def typo_bundle():
    module = load_module(
        "T9-typo-correction/advanced_typo_corrector.py",
        "portfolio_typo_corrector",
    )
    data = pd.read_csv(module.DATA_PATH)
    vocabulary = sorted(data["correct_word"].dropna().astype(str).unique().tolist())
    return module, vocabulary


def correct_text(text: str) -> dict[str, Any]:
    module, vocabulary = typo_bundle()
    corrections = []
    corrected_words = []

    for original in text.split():
        normalized = original.lower()
        if len(normalized) <= 2 or normalized in vocabulary:
            corrected_words.append(original)
            continue

        suggestions = module.suggest_correction(normalized, vocabulary, top_n=3)
        if suggestions:
            replacement = suggestions[0][0]
            corrected_words.append(replacement)
            corrections.append(
                {
                    "input": original,
                    "replacement": replacement,
                    "candidates": [
                        {"word": word, "score": float(score)}
                        for word, score in suggestions
                    ],
                }
            )
        else:
            corrected_words.append(original)

    return {
        "input": text,
        "corrected": " ".join(corrected_words),
        "corrections": corrections,
    }


@lru_cache
def fraud_bundle():
    module = load_module(
        "bank-transaction-fraud-detection/fraud_detection.py",
        "portfolio_fraud",
    )
    artifact = read_json("bank-transaction-fraud-detection/artifacts/results.json")
    data = pd.read_csv(module.DATA_PATH)
    X = data.drop(columns="is_fraud")
    y = data["is_fraud"]

    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=8,
        min_samples_leaf=4,
        class_weight=None,
        random_state=module.RANDOM_STATE,
        n_jobs=-1,
    )
    pipeline = module.build_pipeline(model)
    pipeline.fit(X, y)

    return module, pipeline, float(artifact["selection"]["threshold"]), data, artifact


def fraud_examples() -> dict[str, Any]:
    _, _, _, data, _ = fraud_bundle()
    low = data[data["is_fraud"] == 0].iloc[0].drop(labels=["is_fraud"]).to_dict()
    high = data[data["is_fraud"] == 1].iloc[0].drop(labels=["is_fraud"]).to_dict()
    return {"low_risk": json_safe(low), "high_risk": json_safe(high)}


def predict_fraud(transaction: dict[str, Any]) -> dict[str, Any]:
    module, pipeline, threshold, _, artifact = fraud_bundle()
    prediction = module.predict_transaction(pipeline, threshold, transaction)
    return {
        **prediction,
        "threshold": threshold,
        "risk_band": risk_band(prediction["fraud_probability"], threshold),
        "benchmark": artifact["test_metrics"],
        "model_note": (
            "Interactive model is refit on the full synthetic dataset using the "
            "validation-selected configuration. Benchmark metrics remain from the held-out test split."
        ),
    }


@lru_cache
def credit_bundle():
    module = load_module(
        "credit-repayment-prediction/train.py",
        "portfolio_credit",
    )
    artifact = read_json("credit-repayment-prediction/artifacts/results.json")
    data = pd.read_csv(module.DATA_PATH)
    X = data.drop(columns=["customer_id", "is_refunded"])
    y = data["is_refunded"]

    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=10,
        min_samples_leaf=1,
        random_state=module.RANDOM_STATE,
        n_jobs=-1,
    )
    pipeline = module.build_pipeline(model)
    pipeline.fit(X, y)
    return pipeline, data, artifact


def credit_examples() -> dict[str, Any]:
    _, data, _ = credit_bundle()
    low = (
        data[data["is_refunded"] == 0]
        .iloc[0]
        .drop(labels=["customer_id", "is_refunded"])
        .to_dict()
    )
    high = (
        data[data["is_refunded"] == 1]
        .iloc[0]
        .drop(labels=["customer_id", "is_refunded"])
        .to_dict()
    )
    return {"low_probability": json_safe(low), "high_probability": json_safe(high)}


def predict_credit(customer: dict[str, Any]) -> dict[str, Any]:
    pipeline, _, artifact = credit_bundle()
    probability = float(pipeline.predict_proba(pd.DataFrame([customer]))[0, 1])
    return {
        "repayment_probability": probability,
        "prediction": int(probability >= 0.5),
        "risk_band": repayment_band(probability),
        "benchmark": artifact["test_metrics"],
        "model_note": (
            "Interactive model is refit on the full synthetic dataset using the "
            "validation-selected configuration. Benchmark metrics remain from the held-out test split."
        ),
    }


def rag_evaluation() -> dict[str, Any]:
    retrieval = read_json("llm-knowledge-base-assistant/eval/results.json")
    threshold = read_json("llm-knowledge-base-assistant/eval/threshold.json")
    return {
        "retrieval": retrieval,
        "abstention": {
            key: threshold[key]
            for key in (
                "threshold",
                "balanced_accuracy",
                "answerable_recall",
                "unanswerable_recall",
                "embedding_model",
                "embedding_revision",
            )
        },
    }


async def rag_status() -> dict[str, Any]:
    url = os.getenv("RAG_SERVICE_URL")
    if not url:
        return {
            "configured": False,
            "available": False,
            "detail": "Set RAG_SERVICE_URL or start the Docker Compose rag profile.",
        }

    try:
        async with httpx.AsyncClient(timeout=2.0) as client:
            response = await client.get(f"{url.rstrip('/')}/health")
            response.raise_for_status()
            return {
                "configured": True,
                "available": True,
                "service": response.json(),
            }
    except (httpx.HTTPError, ValueError) as exc:
        return {
            "configured": True,
            "available": False,
            "detail": str(exc),
        }


async def ask_rag(question: str, top_k: int) -> dict[str, Any]:
    url = os.getenv("RAG_SERVICE_URL")
    if not url:
        raise RuntimeError("RAG service is not configured.")

    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(
            f"{url.rstrip('/')}/ask",
            json={"question": question, "top_k": top_k},
        )
        response.raise_for_status()
        return response.json()


def risk_band(probability: float, threshold: float) -> str:
    if probability >= max(0.7, threshold * 2):
        return "high"
    if probability >= threshold:
        return "review"
    return "low"


def repayment_band(probability: float) -> str:
    if probability >= 0.75:
        return "high"
    if probability >= 0.5:
        return "medium"
    return "low"


def json_safe(record: dict[str, Any]) -> dict[str, Any]:
    safe = {}
    for key, value in record.items():
        if pd.isna(value):
            safe[key] = None
        elif hasattr(value, "item"):
            safe[key] = value.item()
        else:
            safe[key] = value
    return safe
