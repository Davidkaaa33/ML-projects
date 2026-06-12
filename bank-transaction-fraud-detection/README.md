# Bank Transaction Fraud Detection

A machine learning project that classifies bank transactions as **normal** or **fraudulent**.

## Dataset

This project uses a synthetic bank transaction dataset.

Labels:
- `0` — normal transaction
- `1` — fraudulent transaction

Features:
- `transaction_amount`
- `sender_country`
- `recipient_country`
- `customer_age`
- `risk_segment`
- `account_balance`
- `avg_transaction_amount`
- `transaction_type`
- `device_type`
- `previous_failed_attempts`
- `transactions_last_24h`
- `days_since_last_transaction`
- `time_by_greenwich`

## Technologies

- Python
- pandas
- numpy
- scikit-learn
- matplotlib
- seaborn

## Project Steps

1. Load the dataset
2. Explore the data
3. Check fraud and normal transaction distribution
4. Create new fraud detection features
5. Convert categorical columns into numerical features
6. Split data into train and test sets
7. Train machine learning models
8. Compare model performance
9. Evaluate the best model
10. Test custom transactions

## Metrics

- Accuracy
- Precision
- Recall
- F1-score
- ROC-AUC
- Confusion Matrix

## Status
Completed.

The project can:
- load and prepare the transaction dataset
- analyze fraud and normal transaction distribution
- create new features from transaction behavior
- convert categorical features into numerical features
- train fraud detection models
- compare model performance using classification metrics
- predict whether a new transaction is normal or fraudulent
- output fraud probability for custom transactions
