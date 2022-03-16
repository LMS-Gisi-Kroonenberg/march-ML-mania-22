import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.linear_model import LogisticRegression


###
TRAINING_DATA_URL = 'training_data.csv'
FEATURE_COUNT = 15  # Assume features come before class in column list.
###


###
def print_results(true, predicted):
    print('Confusion Matrix:')
    print(confusion_matrix(true, predicted))
    print('Accuracy:\t' + str(accuracy_score(true, predicted)))
    return accuracy_score(true, predicted)
###


training_data = pd.read_csv(TRAINING_DATA_URL)

# Create arrays for features and classes.
X = training_data.drop('Outcome', axis=1)
y = training_data.drop(set(training_data).difference({'Outcome'}), axis=1)

# Get training and test folds.
# split data into 2 folds for training and test
X_trainFold1, X_testFold1, y_trainFold1, y_testFold1 = train_test_split(X, y, test_size=0.25, random_state=1)
X_trainFold2 = X_testFold1
X_testFold2 = X_trainFold1
y_trainFold2 = y_testFold1
y_testFold2 = y_trainFold1
y_true = np.concatenate([y_testFold1, y_testFold2])

# Logistic Regression
lr_model = LogisticRegression(max_iter=10000)
lr_model.fit(X_trainFold1, y_trainFold1)
lr_pred_fold1 = lr_model.predict(X_testFold1)
lr_model.fit(X_trainFold2, y_trainFold2)
lr_pred_fold2 = lr_model.predict(X_testFold2)
lr_y_pred = np.concatenate([lr_pred_fold1, lr_pred_fold2])

print('Logistic Regression')
print_results(y_true, lr_y_pred)

