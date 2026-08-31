# Credit Repayment Prediction

## Problem

Predict whether a customer will repay a credit. The included synthetic dataset has 5,000 rows: 3,342 positive repayment outcomes and 1,658 negative outcomes. Its legacy target column is named `is_refunded`; the project interprets it as repayment status.

## Preprocessing and models

`train.py` removes the identifier, one-hot encodes employment status, loan purpose, and payment method, and keeps numeric credit and customer features. Preprocessing is learned inside an sklearn Pipeline. Logistic Regression provides a linear baseline and Random Forest models nonlinear relationships.

## Validation

A stratified 60/20/20 train/validation/test split preserves the target ratio. Logistic Regression and a small Random Forest parameter set are compared on validation ROC-AUC. The test split remains untouched until the model and parameters are selected.

## Results

Best configuration per model on validation:

| Model | ROC-AUC | Accuracy | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|
| Logistic Regression (`C=1.0`) | 0.8917 | 0.8360 | 0.8652 | 0.8937 | 0.8792 |
| Random Forest (`max_depth=10`, `min_samples_leaf=1`) | 0.9521 | 0.8860 | 0.8837 | 0.9551 | 0.9180 |

Random Forest was selected. Final untouched test results are ROC-AUC **0.9550**, accuracy **0.8870**, precision **0.9075**, recall **0.9251**, and F1 **0.9162**.

The ten highest Random Forest importances are:

| Feature | Importance |
|---|---:|
| previous refunds | 0.2753 |
| late payments | 0.1767 |
| credit score | 0.1304 |
| support tickets | 0.1023 |
| credit amount | 0.0715 |
| income | 0.0485 |
| days since credit | 0.0482 |
| customer age | 0.0408 |
| previous loans | 0.0260 |
| employment status: unemployed | 0.0083 |

Importances describe how much the fitted forest used each feature; they do not establish causal effects.

## Run

```bash
cd credit-repayment-prediction
pip install -r requirements.txt
python train.py
```

The dataset is synthetic, and the single fixed validation split makes model comparison less stable than repeated cross-validation.
