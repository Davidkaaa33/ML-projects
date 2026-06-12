# Credit Refund Prediction

A beginner machine learning project that predicts whether a customer credit will be **refunded** or **not refunded**.

## Dataset

This project uses a synthetic credit refund dataset.

Target:

* `0` — credit will not be refunded
* `1` — credit will be refunded

Features include:

* credit amount
* customer age
* credit score
* income
* employment status
* loan purpose
* previous loans
* previous refunds
* late payments
* days since credit
* support tickets
* payment method

## Technologies

* Python
* pandas
* numpy
* scikit-learn
* matplotlib
* Random Forest

## Project Steps

1. Load the dataset
2. Explore the data
3. Prepare features and target
4. Convert categorical columns into numerical features
5. Split data into train and test sets
6. Train a Random Forest model
7. Evaluate the model
8. Check feature importance
9. Test predictions on new customer examples

## Metrics

* Accuracy
* Precision
* Recall
* F1-score
* ROC-AUC
* Confusion Matrix

## Status

In progress.

The project can:

* load and prepare the dataset
* split data into train and test sets
* convert categorical features into numerical features
* train a Random Forest classification model
* evaluate the model using accuracy, precision, recall, F1-score and ROC-AUC
* show which features are most important for refund prediction
* predict whether a new credit case may be refunded
