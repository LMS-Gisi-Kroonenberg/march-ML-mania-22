import numpy as np
from pandas import read_csv, unique
import csv

url = 'data/MDataFiles_Stage2/MRegularSeason03DetailedResults.csv'
names = ['Season','DayNum','WTeamID','WScore','LTeamID','LScore','WLoc','NumOT','WFGM','WFGA','WFGM3','WFGA3','WFTM','WFTA','WOR','WDR','WAst','WTO','WStl','WBlk','WPF','LFGM','LFGA','LFGM3','LFGA3','LFTM','LFTA','LOR','LDR','LAst','LTO','LStl','LBlk','LPF']
dataset = read_csv(url, skiprows=1, names=names)

N_teams = len(unique(dataset.sort_values('WTeamID')['WTeamID']))

teams = {}
# team[team_ID] = [GAMES PLAYED, AVG SCORE, FGM, FGA, FGM3, FGA3, FTM, FTA, OR, DR, AST, TO, STL, BLK, PF]
for i in range(N_teams):
    teams.update({unique(dataset.sort_values('WTeamID')['WTeamID'])[i]: np.zeros(15)})

# Add gross stats throughout season
for game in dataset.values:
    W_id = game[2]
    L_id = game[4]
    
    W_stats = [1, game[3], game[8], game[9], game[10], game[11], game[12], game[13], game[14], game[15], game[16], game[17], game[18], game[19], game[20]]
    L_stats = [1, game[5], game[21], game[22], game[23], game[24], game[25], game[26], game[27], game[28], game[29], game[18], game[31], game[32], game[33]]
    teams[W_id] = np.add(teams[W_id], W_stats)
    teams[L_id] = np.add(teams[L_id], L_stats)

# Take average stats per game
for id in teams:
    teams[id] = teams[id]/teams[id][0]

# Export to csv
csv_columns = ['ID','Score','FGM', 'FGA', 'FGM3', 'FGA3', 'FTM', 'FTA', 'OR', 'DR', 'AST', 'TO', 'STL', 'BLK', 'PF']
csv_file = "2003_stats.csv"

try:
    with open(csv_file, 'w') as f:
        # CSV header
        writer = csv.DictWriter(f, fieldnames=csv_columns)
        writer.writeheader()

        # Write a line of stats for each team
        for key in teams.keys():
            X = np.insert(teams[key], 0, key, axis=0)
            arr_str = ''
            for i in range(len(X)):
                if i == 1:
                    continue
                arr_str = arr_str + str(X[i])
                if i != len(X) - 1:
                    arr_str = arr_str + ','
            arr_str = arr_str + '\n'
            f.write(arr_str)
except IOError:
    print("I/O error")