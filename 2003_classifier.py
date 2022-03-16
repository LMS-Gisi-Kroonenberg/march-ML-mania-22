import numpy as np
import math
import random
from numpy import array, mean, cov
from numpy.linalg import eig
from pandas import read_csv
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier

def print_results(true, predicted):
    print('Confusion Matrix:')
    print(confusion_matrix(true, predicted))
    print('Accuracy:\t' + str(accuracy_score(true, predicted)))
    return accuracy_score(true, predicted)

def pr_accept(i, old_acc, new_acc):
    c = 1
    return pow(math.e, -((i/c)*((old_acc-new_acc)/old_acc)))

def ftr_names(idx_arr):
    ret_arr = np.array([])
    # Modified
    names = ['Score1','FGM1','FGA1','FGM31','FGA31','FTM1','FTA1','OR1','DR1','AST1','TO1','STL1','BLK1','PF1','Score2','FGM2','FGA2','FGM32','FGA32','FTM2','FTA2','OR2','DR2','AST2','TO2','STL2','BLK2','PF2','zScore1','zFGM1','zFGA1','zFGM31','zFGA31','zFTM1','zFTA1','zOR1','zDR1','zAST1','zTO1','zSTL1','zBLK1','zPF1','zScore2','zFGM2','zFGA2','zFGM32','zFGA32','zFTM2','zFTA2','zOR2','zDR2','zAST2','zTO2','zSTL2','zBLK2','zPF2',]
    #names = ['sepal-length', 'sepal-width', 'petal-length', 'petal-width', 'z1', 'z2', 'z3', 'z4']
    idx_arr = np.sort(idx_arr)
    for idx in idx_arr:
        ret_arr = np.append(ret_arr, names[int(idx)])
    return ret_arr

def get_removed(set):
    all = np.array(range(56)) # Modified
    rmvd = np.array([])
    for ftr in all:
        if ftr not in set:
            rmvd = np.append(rmvd, ftr)
    return rmvd

def get_new(set):
    rmvd = get_removed(set)
    return random.choice(rmvd)

def find_min_idx(set):
    min = 0
    for i in range(len(set)):
        if set[i][0] < set[min][0]:
            min = i
    return min

def find_max_idx(set):
    min = 0
    for i in range(len(set)):
        if set[i][0] > set[min][0]:
            min = i
    return min

def print_best(best_sets):
    sorted_best = sorted(best_sets, key=lambda x: x[0], reverse=True)
    for i in range(len(sorted_best)):
        print('\t' + str(i+1) + '.')
        print('\t\tFeatures: ' + str(ftr_names(sorted_best[i][1])))
        print('\t\tAccuracy: ' + str(sorted_best[i][0]))

def dup_exists(sample, set):
    sample = np.sort(sample)
    for i in range(len(set)):
        set[i][1] = np.sort(set[i][1])
        if np.array_equal(set[i][1], sample):
            return True
    return False

# load dataset
TOURNEY_YEAR = '2003'
games_url = 'data/MDataFiles_Stage2/2003TourneyCompact.csv'
games_names = ['Team1ID','Team2ID','Outcome']
stats_url = 'all_reg_season_team_stats.csv'
stats_names = ['ID','Score','FGM','FGA','FGM3','FGA3','FTM','FTA','OR','DR','AST','TO','STL','BLK','PF', 'WinPCT', 'Games']
classes=[0, 1]

# Team IDs, outcome
dataset_abrv = read_csv(games_url, skiprows=1, names=games_names).values
# Stats for each team
stats = read_csv(stats_url, skiprows=1, names=stats_names)

# Create expanded dataset with team stats and game outcome
dataset = np.empty((len(dataset_abrv), 29))
for i in range(len(dataset_abrv)):
    t1_id = str(dataset_abrv[i][0]) + '_' + TOURNEY_YEAR
    t2_id = str(dataset_abrv[i][1]) + '_' + TOURNEY_YEAR
    t1_stats = stats.loc[stats['ID'] == t1_id]
    t2_stats = stats.loc[stats['ID'] == t2_id]

    dataset[i][0:14] = t1_stats.values[0][1:15]
    dataset[i][14:28] = t2_stats.values[0][1:15]
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
print()

# Data transformation

# Calculate the mean of each column
M = mean(X.T, axis=1)
# Center columns
C = X - M
# Calculate covariance matrix of centered matrix
V = cov(C.T.astype(float))
values, vectors = eig(V)
# print('eigenvectors:\n' + str(vectors))
# print('eigenvalues:\n' + str(values))
# print('PoV:\t' + str(values[0]/np.sum(values)))

#project data
P = vectors.T.dot(C.T)
Z = P.T
# Select a subset of transformed features such that PoV > 0.9
z1 = [[i[0]] for i in Z]

Z_trainFold1, Z_testFold1, y_trainFold1, y_testFold1 = train_test_split(z1, y, test_size=0.50, random_state=1)
Z_trainFold2 = Z_testFold1
Z_testFold2 = Z_trainFold1
y_trainFold2 = y_testFold1
y_testFold2 = y_trainFold1
y_true = np.concatenate([y_testFold1, y_testFold2])

# Neural Net
svm_model = MLPClassifier(max_iter=10000) # Increase maximum interation count to resolve convergence issue
svm_model.fit(Z_trainFold1, y_trainFold1)
svm_pred_fold1 = svm_model.predict(Z_testFold1)
svm_model.fit(Z_trainFold2, y_trainFold2)
svm_pred_fold2 = svm_model.predict(Z_testFold2)
svm_y_pred = np.concatenate([svm_pred_fold1, svm_pred_fold2])
PCA_acc = print_results(y_true, svm_y_pred)
print('Features:\t[\'z1\']')

# Concatenate original and transformed features

print('\nSimulated Annealing')
x_all = np.concatenate((X,Z), axis=1)
x_all_copy = x_all
x_all_len = len(X)
removed = np.array([])
current_set = np.array(range(56))
feature_count = len(current_set)
accepted = np.array([])
best_acc = PCA_acc
best_set = current_set

restart_counter = 0
# Track set and accuracy score from the last improved set (to restart to if necessary)
prev_acc = best_acc

for i in range(100):
    r1 = random.random()
    num_modified = round((r1 % 2) + 1)
    if len(removed) == 1:
        num_modified = 1

    r2 = random.random()
    # Randomly remove/add features
    if len(current_set) == feature_count:
        # Remove if current set is full
        to_rmv = random.sample(list(current_set), num_modified)
        removed = np.concatenate([removed, to_rmv])
        for element in to_rmv:
            if element in current_set:
                idx = np.argwhere(current_set==element)
                current_set = np.delete(current_set, idx)
    elif len(current_set) <= num_modified:
        # Add if set is too small
        to_add = random.sample(list(removed), num_modified)
        current_set = np.concatenate([current_set, to_add])
        for element in to_add:
            if element in removed:
                idx = np.argwhere(removed==element)
                removed = np.delete(removed, idx)
    elif random.choice([0, 1]):
        # Random add
        to_add = random.sample(list(removed), num_modified)
        current_set = np.concatenate([current_set, to_add])
        for element in to_add:
            if element in removed:
                idx = np.argwhere(removed==element)
                removed = np.delete(removed, idx)
    else:
        # Random remove
        to_rmv = random.sample(list(current_set), num_modified)
        removed = np.concatenate([removed, to_rmv])
        for element in to_rmv:
            if element in current_set:
                idx = np.argwhere(current_set==element)
                current_set = np.delete(current_set, idx)

    to_test = np.empty([len(x_all),len(current_set)])
    removed = np.sort(removed)[::-1]

    # Apply modifications
    for j in range(len(x_all)):
        temp = x_all[j]
        for elem in removed:
            temp = np.delete(temp, int(elem))
        to_test[j] = temp

    # split data into 2 folds for training and test modified feature set
    X_trainFold1, X_testFold1, y_trainFold1, y_testFold1 = train_test_split(to_test, y, test_size=0.50, random_state=1)
    X_trainFold2 = X_testFold1
    X_testFold2 = X_trainFold1
    y_trainFold2 = y_testFold1
    y_testFold2 = y_trainFold1
    y_true = np.concatenate([y_testFold1, y_testFold2])

    # Neural Net
    nn_model = MLPClassifier(max_iter=10000) # Increase maximum interation count to resolve convergence issue
    nn_model.fit(X_trainFold1, y_trainFold1)
    nn_pred_fold1 = nn_model.predict(X_testFold1)
    nn_model.fit(X_trainFold2, y_trainFold2)
    nn_pred_fold2 = nn_model.predict(X_testFold2)
    nn_y_pred = np.concatenate([nn_pred_fold1, nn_pred_fold2])
    current_acc = accuracy_score(y_true, nn_y_pred)
    current_confusion = confusion_matrix(y_true, nn_y_pred)

    print('\n' + str(i) + ')')
    prob_accept = pr_accept(i,best_acc,current_acc)
    rand_uniform = random.uniform(0,1)

    if prev_acc <= current_acc: #TODO: equal to for first set?
        status = '\033[32mIMPROVED\033[0m'
        rand_uniform = '-'
        prob_accept = '-'
        if best_acc <= current_acc:
            best_acc = current_acc
            best_set = current_set
            best_confusion = current_confusion
            restart_counter = 0
        else:
            restart_counter+=1
        prev_acc = current_acc
        prev_set = current_set
        # Change current subset to new best subset
    elif rand_uniform > prob_accept:
        restart_counter+=1
        status = '\033[31mDISCARDED\033[0m'
    else:
        restart_counter+=1
        status = '\033[33mACCEPTED\033[0m'
        prev_acc = current_acc
        prev_set = current_set
    # Log current as prev for comparison on next iteration
    if restart_counter == 10:
        current_acc = best_acc
        current_set = best_set
        prev_acc = current_acc
        prev_set = current_acc
        removed = get_removed(current_set)
        restart_counter = 0
        status = '\033[31mRESTART\033[0m'
    print('\tFeatures:\t' + str(ftr_names(current_set)))
    print('\tAccuracy:\t' + str(current_acc))
    print('\tPr[accept]:\t' + str(prob_accept))
    print('\tRand Uniform:\t' + str(rand_uniform))
    print('\tRestart Val:\t' + str(restart_counter))
    print('\tStatus:\t\t' + str(status))
print('\nFinal Feature Set (Simulated Annealing):')
print('Confusion Matrix:')
print(best_confusion)
print('Accuracy:\t' + str(best_acc))
print('Features:\t' + str(ftr_names(best_set)))
print('Removed:\t' + str(ftr_names(get_removed(best_set))))

# Genetic Algorithm
print('\nGenetic Algorithm')
quit()
n = 5
# feature       idx
# sepal-length   0
# sepal-width    1
# petal-length   2
# petal-width    3
# z1             4
# z2             5
# z3             6
# z4             7
population =[[4,0,1,2,3],[4,5,1,2,3],[4,5,6,1,2],[4,5,6,7,1],[4,5,6,7,0]]
init_size = len(population)

for trial in range(50):
    best = [[0,[], None] for _ in range(n)]
    # Crossover
    cross_pop = population
    for j in range(init_size):
        for k in range(j+1,init_size):
            union = np.union1d(population[j], population[k])
            intersection = np.intersect1d(population[j], population[k])
            if(len(union) != 0):
                cross_pop.append(union)
            if(len(intersection) != 0):
                cross_pop.append(intersection)
    # Mutation
    mut_pop = cross_pop.copy()
    for j in range(len(mut_pop)):
        mut_choice = random.randrange(3)
        if (mut_choice == 0 and len(mut_pop[j]) != 8) or len(mut_pop[j]) == 0:
            # Add new feature
            new = get_new(mut_pop[j])
            mut_pop[j] = np.append(mut_pop[j], new)
        elif (mut_choice == 1 and len(mut_pop[j]) > 1) or len(mut_pop[j]) == 8:
            # Remove feature
            rmv = np.where(mut_pop[j] == random.choice(mut_pop[j]))
            mut_pop[j] = np.delete(mut_pop[j], rmv)
        else:
            # Replace feature
            rmvd = get_removed(mut_pop[j])
            mut_pop[j] = np.delete(mut_pop[j], np.where(mut_pop[j] == random.choice(mut_pop[j])))
            mut_pop[j] = np.append(mut_pop[j], random.choice(rmvd))

    to_test = [0] * len(x_all)
    population = mut_pop + cross_pop

    # Evaluation
    for i in range(len(population)):
        removed = get_removed(population[i])
        removed = np.sort(removed)[::-1]
        for j in range(len(x_all)):
            temp = x_all[j]
            for elem in removed:
                temp = np.delete(temp, int(elem))
            to_test[j] = temp
        # split data into 2 folds for training and test modified feature set
        X_trainFold1, X_testFold1, y_trainFold1, y_testFold1 = train_test_split(to_test, y, test_size=0.50, random_state=1)
        X_trainFold2 = X_testFold1
        X_testFold2 = X_trainFold1
        y_trainFold2 = y_testFold1
        y_testFold2 = y_trainFold1
        y_true = np.concatenate([y_testFold1, y_testFold2])


        nn_model = MLPClassifier(max_iter=10000) # Increase maximum interation count to resolve convergence issue
        nn_model.fit(X_trainFold1, y_trainFold1)
        nn_pred_fold1 = nn_model.predict(np.array(X_testFold1, dtype=float)) # Resolves dtype issues with predict
        nn_model.fit(X_trainFold2, y_trainFold2)
        nn_pred_fold2 = nn_model.predict(np.array(X_testFold2, dtype=float))
        nn_y_pred = np.concatenate([nn_pred_fold1, nn_pred_fold2])
        current_acc = accuracy_score(y_true, nn_y_pred)

        min_idx = find_min_idx(best)
        if best[min_idx][0] < current_acc and not dup_exists(population[i], best):
            best[min_idx][0] = current_acc
            best[min_idx][1] = population[i]
            best[min_idx][2] = confusion_matrix(y_true, svm_y_pred)
    print(str(trial) + ')')
    print_best(best)
    # Selection
    new_pop = [[[]] for _ in range(n)]
    for j in range(len(best)):
        new_pop[j] = best[j][1]
    # print('trial ' + str(trial) + ' best: ' + str(new_pop))
    population = new_pop
best_idx = find_max_idx(best)

print('\nFinal Feature Set (Genetic Algorithm):')
print('Confusion Matrix:')
print(best[best_idx][2]) # TODO
print('Accuracy:\t' + str(best[best_idx][0]))
print('Features:\t' + str(ftr_names(best[best_idx][1])))
