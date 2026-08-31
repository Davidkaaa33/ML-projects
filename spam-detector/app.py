from pathlib import Path

import joblib
from fastapi import FastAPI
from pydantic import BaseModel


MODEL_PATH = Path(__file__).parent / "model.joblib"
pipeline = joblib.load(MODEL_PATH)
app = FastAPI(title="SMS Spam Detector")


class Message(BaseModel):
    text: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
def predict(message: Message):
    probabilities = pipeline.predict_proba([message.text])[0]
    spam_index = list(pipeline.classes_).index("spam")
    label = pipeline.predict([message.text])[0]
    return {"label": label, "spam_probability": float(probabilities[spam_index])}
