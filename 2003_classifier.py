import numpy as np
from pandas import read_csv
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier

def print_results(true, predicted):
    print('Accuracy Score:')
    print(accuracy_score(true, predicted))
    print('Confusion Matrix:')
    print(confusion_matrix(true, predicted))

# load dataset
games_url = 'data/MDataFiles_Stage2/2003TourneyCompact.csv'
games_names = ['Team1ID','Team2ID','Outcome']
stats_url = '2003_stats.csv'
stats_names = ['ID','Score','FGM','FGA','FGM3','FGA3','FTM','FTA','OR','DR','AST','TO','STL','BLK','PF']
classes=[0, 1]

# Team IDs, outcome
dataset_abrv = read_csv(games_url, skiprows=1, names=games_names).values
# Stats for each team
stats = read_csv(stats_url, skiprows=1, names=stats_names)

# Create expanded dataset with team stats and game outcome
dataset = np.empty((len(dataset_abrv), 29))
for i in range(len(dataset_abrv)):
    t1_id = dataset_abrv[i][0]
    t2_id = dataset_abrv[i][1]
    t1_stats = stats.loc[stats['ID'] == t1_id]
    t2_stats = stats.loc[stats['ID'] == t2_id]

    dataset[i][0:14] = t1_stats.values[0][1:]
    dataset[i][14:28] = t2_stats.values[0][1:]
    dataset[i][28] = dataset_abrv[i][2]

# create arrays for features and classes
array = dataset
X = array[:,0:28]
y = array[:,28]

# split data into 2 folds for training and test
X_trainFold1, X_testFold1, y_trainFold1, y_testFold1 = train_test_split(X, y, test_size=0.50, random_state=1)
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

# Neural Net
nn_model = MLPClassifier(max_iter=100000)
nn_model.fit(X_trainFold1, y_trainFold1)
nn_pred_fold1 = nn_model.predict(X_testFold1)
nn_model.fit(X_trainFold2, y_trainFold2)
nn_pred_fold2 = nn_model.predict(X_testFold2)
nn_y_pred = np.concatenate([nn_pred_fold1, nn_pred_fold2])
print('\nNeural Net')
print_results(y_true, nn_y_pred)