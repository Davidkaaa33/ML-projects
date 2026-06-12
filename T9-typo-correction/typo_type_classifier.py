import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 1000)
pd.set_option("display.max_rows", 100)

df = pd.read_csv('data/t9_typo_correction_dataset.csv')
X = df[['edit_distance', 'word_length', 'typo_length', 'length_difference', 'same_first_letter', 'is_last_letter_error']]
X = pd.get_dummies(df[['edit_distance', 'word_length', 'typo_length', 'length_difference', 'same_first_letter', 'is_last_letter_error', 'mistake_position']], drop_first = True)
y = df['typo_type']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 42, stratify = y)
model = RandomForestClassifier(n_estimators = 200, max_depth = 8, random_state = 42)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
# print(classification_report(y_test, y_pred))
# print(confusion_matrix(y_test, y_pred))


new_example_1 = {
        "edit_distance": 1,
        "word_length": 5,
        "typo_length": 4,
        "length_difference": 1,
        "same_first_letter": 1,
        "is_last_letter_error": 1,
        "mistake_position_last1": 1,
        "mistake_position_last2": 0,
        "mistake_position_last3": 0,
        "mistake_position_none": 0
    }
new_example_2 = {
        "edit_distance": 0,
        "word_length": 5,
        "typo_length": 5,
        "length_difference": 0,
        "same_first_letter": 1,
        "is_last_letter_error": 0,
        "mistake_position_last1": 0,
        "mistake_position_last2": 0,
        "mistake_position_last3": 0,
        "mistake_position_none": 1
    }

new_examples = pd.DataFrame([new_example_1, new_example_2])
new_examples = new_examples.reindex(columns = X.columns, fill_value = 0)
new_predictions = model.predict(new_examples)
print(new_predictions)
