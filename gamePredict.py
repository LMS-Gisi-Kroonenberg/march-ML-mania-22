import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn import preprocessing


###
TRAINING_DATA_URL = 'training_data.csv'
FEATURE_COUNT = 15  # Assume features come before class in column list.
TEAM_DATA_URL = 'all_reg_season_team_stats.csv'
RESULT_DATA_URL = 'allResults.csv'
SAMPLE_URL = 'data/MDataFiles_Stage2/MSampleSubmissionStage2.csv'
###


###
def print_results(true, predicted):
    print('Confusion Matrix:')
    print(confusion_matrix(true, predicted))
    print('Accuracy:\t' + str(accuracy_score(true, predicted)))
    return accuracy_score(true, predicted)


def get_win_prob(team1, team2, team_data, model):
    feat = team_data.loc[team1] - team_data.loc[team2]
    feat_df = pd.DataFrame(feat).transpose()
    return "{:.1f}".format(model.predict_proba(feat_df)[0][1]*100)


def make_output(sample_url, output_url, model):
    team_data = pd.read_csv(TEAM_DATA_URL, index_col=0).drop('Games', axis=1)

    sample_df = pd.read_csv(sample_url)
    sample_df['Pred'] = sample_df.apply(lambda row: get_win_prob(
        row.ID.split('_')[1]+'_'+'2022',
        row.ID.split('_')[2]+'_'+'2022',
        team_data,
        model
    ), axis=1)

    sample_df.to_csv(path_or_buf=output_url, index=None)
    print('Saved output to', output_url)


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

"""
# Scale data to have zero mean and unit variance for NN.
scaler1 = preprocessing.StandardScaler().fit(X_trainFold1)
X_trainFold1 = scaler1.transform(X_trainFold1)
X_testFold1 = scaler1.transform(X_testFold1)

scaler2 = preprocessing.StandardScaler().fit(X_trainFold2)
X_trainFold2 = scaler2.transform(X_trainFold2)
X_testFold2 = scaler2.transform(X_testFold2)

# print(X_trainFold1.mean(axis=0))
# print(X_trainFold2.mean(axis=0))
"""

# Logistic Regression, accuracy 0.74
lr_model = LogisticRegression(max_iter=10000)
lr_model.fit(X_trainFold1, y_trainFold1.values.ravel())
lr_pred_fold1 = lr_model.predict(X_testFold1)
lr_model.fit(X_trainFold2, y_trainFold2.values.ravel())
lr_pred_fold2 = lr_model.predict(X_testFold2)
lr_y_pred = np.concatenate([lr_pred_fold1, lr_pred_fold2])

print('Logistic Regression')
print_results(y_true, lr_y_pred)

make_output(SAMPLE_URL, 'lr_output.csv', lr_model)

"""
# Neural Net, accuracy 0.71
nn = MLPClassifier(max_iter=10000, solver='lbfgs', random_state=1)
nn.fit(X_trainFold1, y_trainFold1.values.ravel())
nn_pred_fold1 = nn.predict(X_testFold1)
nn.fit(X_trainFold2, y_trainFold2.values.ravel())
nn_pred_fold2 = nn.predict(X_testFold2)
nn_pred = np.concatenate([nn_pred_fold1, nn_pred_fold2])

print('\nNeural Net')
print_results(y_true, nn_pred)
"""

