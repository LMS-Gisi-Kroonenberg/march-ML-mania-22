from pandas import read_csv
import numpy as np
import csv

url = 'round32.csv'
names = ['Team1', 'Team2']

pred_url = 'decoded_prediction.csv'
pred_names = ['ID1', 'ID2', 'Pred']

bracket = read_csv(url, skiprows=1, names=names).values
pred = read_csv(pred_url, skiprows=1, names = pred_names)
x = 0
while not len(bracket) == 0:
    round = []

    for matchup in bracket:
        team1 = matchup[0]
        team2 = matchup[1]
        # Try team 1 = ID1
        team1_matchups = pred.loc[pred['ID1'] == team1]
        result = team1_matchups.loc[team1_matchups['ID2'] == team2]['Pred'].values
        # Try team 2 = ID1 if no result is found
        if result.size == 0:
                team2_matchups = pred.loc[pred['ID1'] == team2]
                result = team2_matchups.loc[team2_matchups['ID2'] == team1]['Pred'].values
        result = result[0]
        if result < 0.5: #team2 wins
            #print('{} beats {} with prob. {}'.format(team2,team1,result))
            round.append(team2)
        else:
            round.append(team1)
            #print('{} beats {} with prob. {}'.format(team1,team2,result))
        

    print(round)
    bracket = []
    i = 0
    while i < int(len(round)) - 1:
        bracket.append([round[i],round[i+1]])
        #print('{},{}'.format(i,i+1))
        i = i+2
    # print()
    # print(bracket)
    #quit()