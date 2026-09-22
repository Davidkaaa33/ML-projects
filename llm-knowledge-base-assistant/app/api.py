import json
import logging
import uuid
from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI, HTTPException, Request
from ollama import ResponseError
from pydantic import BaseModel, Field, field_validator

from app.rag import RAGAssistant


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Loading RAG assistant...")

    app.state.assistant = RAGAssistant()

    logger.info("RAG assistant ready.")

    yield

    del app.state.assistant


app = FastAPI(
    title="LLM Knowledge Base Assistant",
    description="Local RAG API using Qwen and FAISS.",
    version="0.1.0",
    lifespan=lifespan,
)


class AskRequest(BaseModel):
    question: str = Field(
        min_length=1,
        max_length=1000,
    )

    top_k: int = Field(
        default=3,
        ge=1,
        le=5,
    )

    @field_validator("question")
    @classmethod
    def validate_question(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Question cannot be empty.")

        return value


class RetrievedSource(BaseModel):
    source: str
    chunk_id: int
    score: float


class TimingMetrics(BaseModel):
    retrieval_seconds: float
    generation_seconds: float
    total_seconds: float


class AskResponse(BaseModel):
    question: str
    answer: str
    retrieved_sources: list[RetrievedSource]
    metrics: TimingMetrics


@app.get("/health")
def health(request: Request):
    store = request.app.state.assistant.retriever.vector_store

    return {
        "status": "ready",
        "indexed_chunks": store.index.ntotal,
    }


@app.post("/ask", response_model=AskResponse)
def ask(payload: AskRequest, request: Request):
    assistant = request.app.state.assistant

    request_id = uuid.uuid4().hex[:12]

    logger.info(
        json.dumps({
            "event": "rag_request_started",
            "request_id": request_id,
            "question_length": len(payload.question),
            "top_k": payload.top_k,
        })
    )

    try:
        result = assistant.ask(
            question=payload.question,
            top_k=payload.top_k,
        )

        logger.info(
            json.dumps({
                "event": "rag_request_completed",
                "request_id": request_id,
                "retrieval_seconds": (
                    result["metrics"]["retrieval_seconds"]
                ),
                "generation_seconds": (
                    result["metrics"]["generation_seconds"]
                ),
                "total_seconds": (
                    result["metrics"]["total_seconds"]
                ),
                "sources": [
                    f"{source['source']}:{source['chunk_id']}"
                    for source in result["retrieved_sources"]
                ],
            })
        )

        return AskResponse(**result)

    except (httpx.RequestError, ResponseError, ConnectionError) as exc:
        logger.exception(
            json.dumps({
                "event": "ollama_unavailable",
                "request_id": request_id,
            })
        )

        raise HTTPException(
            status_code=503,
            detail="Local LLM unavailable. Check Ollama.",
        ) from exc

    except Exception as exc:
        logger.exception(
            json.dumps({
                "event": "rag_request_failed",
                "request_id": request_id,
            })
        )

        raise HTTPException(
            status_code=500,
            detail="Failed to generate an answer.",
        ) from exc
