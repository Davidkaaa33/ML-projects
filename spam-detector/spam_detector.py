import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    confusion_matrix,
    classification_report
)

df = pd.read_csv('data/spam.csv', encoding="latin-1")
df = df[['v1', 'v2']]
df.columns = ['label', 'message']

# print(df.head())
# print(df.shape)                             #5572 * 2
# print(df.info())
# print(df['label'].value_counts())           #ham : 4825, spam : 747
# for c in df.columns:
#     print(c, " : ", df[c].isna().sum())       #label : 0, message : 0

X = df['message']
y = df['label']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 42, stratify = y)
# print(X_train.shape)
# print(X_test.shape)
# print(y_train.shape)
# print(y_test.shape)
# print(y_train.value_counts())
# print(y_test.value_counts())

vectorizer = TfidfVectorizer()
X_train_vectorized = vectorizer.fit_transform(X_train)
X_test_vectorized = vectorizer.transform(X_test)

# print(X_train_vectorized.shape)
# print(X_test_vectorized.shape)

model = MultinomialNB()
model.fit(X_train_vectorized, y_train)
y_pred = model.predict(X_test_vectorized)

print('Accuracy:', accuracy_score(y_test, y_pred))
print('Precision:', precision_score(y_test, y_pred, pos_label = 'spam'))
print('Recall:', recall_score(y_test, y_pred, pos_label = 'spam'))
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))

test_message_1 = 'Congratulations! You won a free prize!'
test_message_2 = 'Hi! Yesterday i sent you accounting from work.'
test_message_3 = 'We tried to connect with You several times to report Your lottery winnings!'
test_message_4 = 'Good afternoon, it is Your Boss. Tomorrow we will have general meeting.'

messages = [test_message_1, test_message_2, test_message_3, test_message_4]


def predict_message(message):
    check_message = [message]
    message_vectorized = vectorizer.transform(check_message)
    predictions = model.predict(message_vectorized)
    print(message, '- prediction:', predictions[0])

for m in messages:
    predict_message(m)