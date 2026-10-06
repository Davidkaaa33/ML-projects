from pathlib import Path

import joblib
from fastapi import FastAPI
from pydantic import BaseModel, Field, field_validator


MODEL_PATH = Path(__file__).parent / "model.joblib"
pipeline = joblib.load(MODEL_PATH)

app = FastAPI(
    title="SMS Spam Detector",
    version="0.1.0",
)


class Message(BaseModel):
    text: str = Field(
        min_length=1,
        max_length=5000,
    )

    @field_validator("text")
    @classmethod
    def validate_text(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Message text cannot be empty.")
        return value


class PredictionResponse(BaseModel):
    label: str
    spam_probability: float


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict", response_model=PredictionResponse)
def predict(message: Message):
    probabilities = pipeline.predict_proba([message.text])[0]
    spam_index = list(pipeline.classes_).index("spam")
    label = pipeline.predict([message.text])[0]

    return PredictionResponse(
        label=label,
        spam_probability=float(probabilities[spam_index]),
    )
