import os
from typing import Any

import httpx
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from pydantic import BaseModel, Field, field_validator

from app.services import (
    ask_rag,
    correct_text,
    credit_examples,
    fraud_examples,
    model_registry,
    predict_credit,
    predict_fraud,
    predict_spam,
    rag_evaluation,
    rag_status,
)


app = FastAPI(
    title="ML Systems Lab API",
    description="Unified inference and evaluation API for the ML engineering portfolio.",
    version="1.0.0",
)

origins = [
    item.strip()
    for item in os.getenv(
        "WEB_ORIGINS",
        "http://localhost:5173,http://localhost:8080",
    ).split(",")
    if item.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


class TextRequest(BaseModel):
    text: str = Field(min_length=1, max_length=5000)

    @field_validator("text")
    @classmethod
    def strip_text(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Text cannot be empty.")
        return value


class RecordRequest(BaseModel):
    record: dict[str, Any]


class RAGRequest(BaseModel):
    question: str = Field(min_length=1, max_length=1000)
    top_k: int = Field(default=3, ge=1, le=5)

    @field_validator("question")
    @classmethod
    def strip_question(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Question cannot be empty.")
        return value


@app.get("/health")
def health():
    return {"status": "ok", "service": "ml-systems-lab-api"}


@app.get("/api/overview")
def overview():
    models = model_registry()
    return {
        "name": "ML Systems Lab",
        "systems": len(models),
        "live_systems": sum(model["live"] for model in models),
        "models": models,
        "quality": {
            "tests": "every project",
            "ci": True,
            "dependency_audit": True,
            "reproducible_metrics": True,
        },
    }


@app.get("/api/models")
def models():
    return model_registry()


@app.get("/api/models/{model_id}")
def model(model_id: str):
    for item in model_registry():
        if item["id"] == model_id:
            return item
    raise HTTPException(status_code=404, detail="Unknown model.")


@app.post("/api/spam/predict")
def spam(payload: TextRequest):
    return predict_spam(payload.text)


@app.post("/api/t9/correct")
def typo(payload: TextRequest):
    return correct_text(payload.text)


@app.get("/api/fraud/examples")
def fraud_example_records():
    return fraud_examples()


@app.post("/api/fraud/predict")
def fraud(payload: RecordRequest):
    try:
        return predict_fraud(payload.record)
    except (KeyError, TypeError, ValueError) as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@app.get("/api/credit/examples")
def credit_example_records():
    return credit_examples()


@app.post("/api/credit/predict")
def credit(payload: RecordRequest):
    try:
        return predict_credit(payload.record)
    except (KeyError, TypeError, ValueError) as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@app.get("/api/rag/evaluation")
def rag_metrics():
    return rag_evaluation()


@app.get("/api/rag/status")
async def rag_service_status():
    return await rag_status()


@app.post("/api/rag/ask")
async def rag_ask(payload: RAGRequest):
    try:
        return await ask_rag(payload.question, payload.top_k)
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except httpx.HTTPError as exc:
        raise HTTPException(
            status_code=503,
            detail="RAG service is configured but unavailable.",
        ) from exc


WEB_DIST = Path(__file__).resolve().parents[2] / "web" / "dist"
if WEB_DIST.exists():
    app.mount(
        "/",
        StaticFiles(directory=WEB_DIST, html=True),
        name="web",
    )
