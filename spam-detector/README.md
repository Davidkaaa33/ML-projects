# SMS Spam Detector

## Dataset

The included `data/spam.csv` is the SMS Spam Collection dataset with 5,572 messages: 4,825 ham and 747 spam.

## Approach

A stratified 80/20 train/test split is used with `random_state=42`. One sklearn Pipeline fits `TfidfVectorizer` followed by `MultinomialNB`, so training, saved-model inference, and the API all use identical text preprocessing.

## Results

| Test metric | Value |
|---|---:|
| Precision | 1.0000 |
| Recall | 0.7047 |
| F1 | 0.8268 |

Confusion matrix, with actual classes as rows and predicted classes as columns:

|  | Predicted ham | Predicted spam |
|---|---:|---:|
| Actual ham | 966 | 0 |
| Actual spam | 44 | 105 |

The error-analysis dataframes contain 0 false positives and 44 false negatives. Printed false negatives include promotional subscription, dating-service, voucher, and premium-rate-call messages. This describes the observed errors without assuming a cause that the examples do not establish.

## Train and inspect errors

```bash
cd spam-detector
pip install -r requirements.txt
python train.py
```

Training prints metrics and representative false-positive/false-negative rows, then saves the complete pipeline as `model.joblib`.

## Inference API

```bash
uvicorn app:app --reload
```

- `GET /health` returns `{"status": "ok"}`.
- `POST /predict` accepts `{"text": "some SMS"}` and returns the predicted label and spam probability.

Docker usage:

```bash
docker build -t spam-detector .
docker run -p 8000:8000 spam-detector
```

The dataset is small and dated, so the measured result should not be treated as performance on current messaging traffic.
