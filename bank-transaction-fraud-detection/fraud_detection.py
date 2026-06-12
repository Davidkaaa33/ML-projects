import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score, precision_score, f1_score, recall_score, confusion_matrix

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 1000)
pd.set_option("display.max_rows", 100)

df = pd.read_csv('data/bank_transactions_fraud_dataset.csv')

df['transaction_time_hour'] = pd.to_datetime(df['time_by_greenwich']).dt.hour

time_zones = {'Germany' : 1, 'Kazakhstan' : 5, 'Russia' : 3, 'Turkey' : 3, 'UAE' : 4, 'China' : 8, 'Unknown' : 0}
df['sender_local_hour'] = df.apply(
    lambda row: (row['transaction_time_hour'] + time_zones.get(row['sender_country'], 0)) % 24, axis = 1
)
df['recipient_local_hour'] = df.apply(
    lambda row: (row['transaction_time_hour'] + time_zones.get(row['recipient_country'], 0)) % 24, axis = 1
)
df['night_transaction'] = ((df['sender_local_hour'].between(0, 6)) & (df['recipient_local_hour'].between(0, 6))).astype(int)

categorical_cols = ['sender_country', 'recipient_country', 'risk_segment', 'transaction_type', 'device_type']
df_encoded = pd.get_dummies(df, columns = categorical_cols, drop_first = False)

X = df_encoded.drop(columns = ['is_fraud', 'time_by_greenwich'])
y = df_encoded['is_fraud']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 42, stratify = y)

n_estimators_list = [100, 200, 300]
max_depth_list = [5, 10, 15]
min_samples_split_list = [2, 5, 10]
min_samples_leaf_list = [1, 2, 4]
results = []
for n_estimators in n_estimators_list:
    for max_depth in max_depth_list:
        for min_samples_split in min_samples_split_list:
            for min_samples_leaf in min_samples_leaf_list:
                model = RandomForestClassifier(n_estimators = n_estimators,
                                               max_depth = max_depth,
                                               min_samples_split = min_samples_split,
                                               min_samples_leaf = min_samples_leaf,
                                               random_state = 42,
                                               n_jobs = -1
                                               )
                model.fit(X_train, y_train)
                y_proba = model.predict_proba(X_test)[:, 1]
                auc = roc_auc_score(y_test, y_proba)
                results.append({'n_estimators' : n_estimators,
                                'max_depth' : max_depth,
                                'min_samples_split' : min_samples_split,
                                'min_samples_leaf' : min_samples_leaf,
                                'roc_auc' : auc
                                })

results_df = pd.DataFrame(results)
best_params = results_df.sort_values(by = 'roc_auc', ascending = False).iloc[0]

best_model = RandomForestClassifier(
    n_estimators = int(best_params['n_estimators']),
    max_depth = int(best_params['max_depth']),
    min_samples_split = int(best_params['min_samples_split']),
    min_samples_leaf = int(best_params['min_samples_leaf']),
    class_weight = {0:1, 1:5},
    random_state = 42,
    n_jobs = -1
)
best_model.fit(X_train, y_train)
y_pred = best_model.predict(X_test)
y_proba = best_model.predict_proba(X_test)[:, 1]
print('ROC_AUC:', roc_auc_score(y_test, y_proba))
print(classification_report(y_test, y_pred))

thresholds = np.arange(0.1, 0.9, 0.05)
results = []
for t in thresholds:
    y_pred_t = (y_proba >= t).astype(int)
    precision = precision_score(y_test, y_pred_t)
    recall = recall_score(y_test, y_pred_t)
    f1 = f1_score(y_test, y_pred_t)
    results.append({
        'threshold' : t,
        'precision' : precision,
        'recall' : recall,
        'f1' : f1
    })
results_df = pd.DataFrame(results)
best_row = results_df.sort_values('f1', ascending = False).iloc[0]
best_threshold = best_row['threshold']

final_pred = (y_proba >= best_threshold).astype(int)
print(classification_report(y_test, final_pred))
print(confusion_matrix(y_test, final_pred))

importance = pd.DataFrame({
    'feature' : X.columns,
    'importance' : best_model.feature_importances_
}).sort_values(by = 'importance', ascending = False)
print(importance.head(10))

test_1 = {
    "customer_age": 35,
    "account_age_days": 1200,
    "account_balance": 50000,
    "avg_transaction_amount": 200,
    "transaction_amount": 150,
    "previous_failed_attempts": 0,
    "transactions_last_24h": 2,
    "days_since_last_transaction": 10,
    "transaction_time_hour": 14,
    "sender_country": "Germany",
    "recipient_country": "Germany",
    "risk_segment": "low",
    "transaction_type": "card_payment",
    "device_type": "mobile"
}
test_2 = {
    "customer_age": 62,
    "account_age_days": 300,
    "account_balance": 12000,
    "avg_transaction_amount": 500,
    "transaction_amount": 4500,
    "previous_failed_attempts": 3,
    "transactions_last_24h": 8,
    "days_since_last_transaction": 1,
    "transaction_time_hour": 2,
    "sender_country": "Russia",
    "recipient_country": "UAE",
    "risk_segment": "high",
    "transaction_type": "online_transfer",
    "device_type": "desktop"
}
test_3 = {
    "customer_age": 28,
    "account_age_days": 600,
    "account_balance": 8000,
    "avg_transaction_amount": 100,
    "transaction_amount": 950,
    "previous_failed_attempts": 1,
    "transactions_last_24h": 5,
    "days_since_last_transaction": 3,
    "transaction_time_hour": 23,
    "sender_country": "Turkey",
    "recipient_country": "China",
    "risk_segment": "medium",
    "transaction_type": "crypto_transfer",
    "device_type": "mobile"
}
test_4 = {
    "customer_age": 45,
    "account_age_days": 2000,
    "account_balance": 100000,
    "avg_transaction_amount": 300,
    "transaction_amount": 280,
    "previous_failed_attempts": 0,
    "transactions_last_24h": 1,
    "days_since_last_transaction": 20,
    "transaction_time_hour": 10,
    "sender_country": "Kazakhstan",
    "recipient_country": "Kazakhstan",
    "risk_segment": "low",
    "transaction_type": "bill_payment",
    "device_type": "pos_terminal"
}

def preprocess_and_predict(test):
    test_df = pd.DataFrame([test])
    test_df['transaction_time_hour'] = test_df['transaction_time_hour']
    test_df['sender_local_hour'] = (test_df['transaction_time_hour'] + test_df['sender_country'].map(time_zones).fillna(0)) % 24
    test_df['recipient_local_hour'] = (test_df['transaction_time_hour'] + test_df['recipient_country'].map(time_zones).fillna(0)) % 24

    test_df = pd.get_dummies(test_df)
    test_df = test_df.reindex(columns = X.columns, fill_value = 0)
    proba = best_model.predict_proba(test_df)[:, 1][0]
    prediction = int(proba >= best_threshold)
    return proba, prediction

for i, t in enumerate([test_1, test_2, test_3, test_4], 1):
    proba, pred = preprocess_and_predict(t)
    if pred == 1:
        label = 'Fraud'
    else:
        label = 'Legal transaction'
    print(f'Test{i} :', pred, '-', label)