import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    recall_score,
    precision_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report
)


pd.set_option("display.max_columns", None)
pd.set_option("display.width", 1000)
pd.set_option("display.max_rows", 100)

df = pd.read_csv('data/credit_refund_dataset.csv')
# print(df.head())
# print(df.info())
# print(df['is_refunded'].value_counts())
# print(df.isna().sum())

X = df.drop(['customer_id', 'is_refunded'], axis = 1)
y = df['is_refunded']
X = pd.get_dummies(X, drop_first = True)
# print(X.head())

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 42, stratify = y)

n_estimators_list = [100, 200, 300]
max_depth_list = [5, 8, 12]
min_samples_split_list = [2, 5]
min_samples_leaf_list = [1, 2, 4]

results = []
best_score = 0
best_model = None
best_params = None
for n_estimators in n_estimators_list:
    for max_depth in max_depth_list:
        for min_samples_split in min_samples_split_list:
            for min_samples_leaf in min_samples_leaf_list:
                model = RandomForestClassifier(n_estimators = n_estimators,
                                               max_depth = max_depth,
                                               min_samples_split = min_samples_split,
                                               min_samples_leaf = min_samples_leaf,
                                               random_state = 42
                                               )
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
                y_proba = model.predict_proba(X_test)[:, 1]

                accuracy = accuracy_score(y_test, y_pred)
                precision = precision_score(y_test, y_pred)
                recall = recall_score(y_test, y_pred)
                f1 = f1_score(y_test, y_pred)
                roc_auc = roc_auc_score(y_test, y_proba)

                results.append({'n_estimators' : n_estimators,
                                'max_depth' : max_depth,
                                'min_samples_split' : min_samples_split,
                                'min_samples_leaf' : min_samples_leaf,
                                'accuracy' : accuracy,
                                'precision' : precision,
                                'recall' : recall,
                                'f1' : f1,
                                'roc_auc' : roc_auc})

                if roc_auc > best_score:
                    best_score = roc_auc
                    best_model = model
                    best_params = {'n_estimators' : n_estimators,
                                   'max_depth' : max_depth,
                                   'min_samples_split' : min_samples_split,
                                   'min_samples_leaf' : min_samples_leaf}

results_df = pd.DataFrame(results)
results_df = results_df.sort_values('roc_auc', ascending = False)
# print(results_df.head(10))

new_customer_1 = {"credit_amount": 5000, "customer_age": 35, "credit_score": 650, "income": 45000, "previous_loans": 1, "previous_refunds": 0,
                  "late_payments": 0, "days_since_credit": 30, "support_tickets": 0, "employment_status_self_employed": 0, "employment_status_student": 0,
                  "employment_status_unemployed": 0, "loan_purpose_education": 0, "loan_purpose_emergency": 0, "loan_purpose_medical": 0,
                  "loan_purpose_shopping": 1, "loan_purpose_travel": 0, "payment_method_card": 1, "payment_method_crypto": 0,"payment_method_paypal": 0}

new_customer_2 = {"credit_amount": 8200, "customer_age": 42, "credit_score": 580, "income": 52000, "previous_loans": 3, "previous_refunds": 1,
                  "late_payments": 3, "days_since_credit": 90, "support_tickets": 2, "employment_status_self_employed": 1, "employment_status_student": 0,
                  "employment_status_unemployed": 0, "loan_purpose_education": 0, "loan_purpose_emergency": 0, "loan_purpose_medical": 0,
                  "loan_purpose_shopping": 0, "loan_purpose_travel": 1, "payment_method_card": 0, "payment_method_crypto": 0,"payment_method_paypal": 1}

new_customer_3 = {"credit_amount": 9300, "customer_age": 29, "credit_score": 480, "income": 28000, "previous_loans": 5, "previous_refunds": 3,
                  "late_payments": 6, "days_since_credit": 180, "support_tickets": 4, "employment_status_self_employed": 0, "employment_status_student": 0,
                  "employment_status_unemployed": 1, "loan_purpose_education": 0, "loan_purpose_emergency": 1, "loan_purpose_medical": 0,
                  "loan_purpose_shopping": 0, "loan_purpose_travel": 0, "payment_method_card": 0, "payment_method_crypto": 1,"payment_method_paypal": 0}

new_customer_4 = {"credit_amount": 1200, "customer_age": 48, "credit_score": 790, "income": 90000, "previous_loans": 2, "previous_refunds": 0,
                  "late_payments": 1, "days_since_credit": 15, "support_tickets": 0, "employment_status_self_employed": 0, "employment_status_student": 0,
                  "employment_status_unemployed": 0, "loan_purpose_education": 0, "loan_purpose_emergency": 0, "loan_purpose_medical": 1,
                  "loan_purpose_shopping": 0, "loan_purpose_travel": 0, "payment_method_card": 0, "payment_method_crypto": 0,"payment_method_paypal": 0}

new_customers = pd.DataFrame([
    new_customer_1,
    new_customer_2,
    new_customer_3,
    new_customer_4
])
new_customers = new_customers.reindex(columns = X.columns, fill_value = 0)
predictions = best_model.predict(new_customers)
probabilities = best_model.predict_proba(new_customers)[:, 1]
for i, prediction in enumerate(predictions, start = 1):
    print(f'№{i}', round(probabilities[i - 1], 4), 'Refunded' if prediction == 1 else 'Not refunded')

plt.bar(range(1, 5), probabilities)
plt.xticks(range(1, 5), ['customer_1', 'customer_2', 'customer_3', 'customer_4'])
plt.ylabel('Refund probability')
plt.show()