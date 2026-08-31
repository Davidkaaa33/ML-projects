# Bank Transaction Fraud Detection

## Problem

Classify bank transactions as normal (`0`) or fraudulent (`1`). Fraud makes up 1,326 of 30,000 rows, so the project prioritizes ranking quality and minority-class performance rather than accuracy.

## Dataset / target

The included synthetic dataset is `data/bank_transactions_fraud_dataset.csv`. The target is `is_fraud`. Inputs describe customer and account history, transaction value and type, device, countries, and Greenwich transaction time.

## Approach

`fraud_detection.py` derives Greenwich hour, sender and recipient local hours, and a night-transaction flag. A single sklearn Pipeline applies this feature engineering, learns one-hot categories from training data, scales numeric inputs for Logistic Regression, and keeps the same transformations for inference.

## Validation strategy

The data is split with stratification into 60% train, 20% validation, and 20% test. Small model configurations, including class weighting, are compared on validation PR-AUC. The final model is selected without test data, and its classification threshold is chosen on validation predictions by maximum F1 over thresholds from 0.05 to 0.95. The untouched test split is evaluated once afterward.

## Models

- Dummy classifier using the training class prior
- Logistic Regression (`C` and `class_weight` compared)
- Random Forest (`max_depth`, `min_samples_leaf`, and `class_weight` compared)

## Results

Best configuration per model on the validation split at the default 0.50 threshold:

| Model | ROC-AUC | PR-AUC | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|
| Dummy baseline | 0.5000 | 0.0442 | 0.0000 | 0.0000 | 0.0000 |
| Logistic Regression | 0.8753 | 0.2719 | 0.1445 | 0.7623 | 0.2429 |
| Random Forest | 0.8973 | 0.3842 | 0.0000 | 0.0000 | 0.0000 |

The final model is Random Forest with `max_depth=8`, `min_samples_leaf=4`, and no class weighting. Validation tuning selected a threshold of **0.15**.

| Final test metric | Value |
|---|---:|
| ROC-AUC | 0.8713 |
| PR-AUC | 0.3399 |
| Precision | 0.3452 |
| Recall | 0.4038 |
| F1 | 0.3722 |

PR-AUC shows how well the model ranks rare fraud cases under class imbalance. Precision describes the share of alerts that are fraud, while recall describes the share of fraud cases caught; together they expose the operational trade-off hidden by accuracy.

## Run

```bash
cd bank-transaction-fraud-detection
pip install -r requirements.txt
python fraud_detection.py
```

The synthetic data does not represent production drift or real fraud costs. The threshold optimizes validation F1, not a business-specific false-positive/false-negative cost.
