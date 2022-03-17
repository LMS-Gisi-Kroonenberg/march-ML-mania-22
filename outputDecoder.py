from pandas import read_csv
import numpy as np
import csv

url = 'lr_output.csv'
names = ['ID', 'Pred']

teams_url = 'data/MDataFiles_Stage2/MTeams.csv'
team_cols = ['TeamID','TeamName','FirstD1Season','LastD1Season']

results = read_csv(url, skiprows=1, names=names).values
teams = read_csv(teams_url, skiprows=1, names = team_cols)

decoded_results = []

for i in range(len(results)):
    ID = results[i][0]
    id1 = round(int(ID[5:-5]))
    id2 = round(int(ID[10:]))
    # Order id1
    if id2 > id1:
        temp = id2
        id2 = id1
        id1 = temp
    team1_str = teams.loc[teams['TeamID'] == id1]['TeamName'].values[0]
    team2_str = teams.loc[teams['TeamID'] == id2]['TeamName'].values[0]
    decoded_results.append([team1_str, team2_str, results[i][1]])

csv_columns = ['ID1', 'ID2', 'Pred']
csv_file = "decoded_prediction.csv"

try:
    with open(csv_file, 'w') as f:
        # CSV header
        writer = csv.DictWriter(f, fieldnames=csv_columns)
        writer.writeheader()
        # Write a line of stats for each team
        for d in decoded_results:
            arr_str = ''
            for i in range(len(d)):
                arr_str = arr_str + str(d[i])
                if i != len(d) - 1:
                    arr_str = arr_str + ','
            arr_str = arr_str + '\n'
            f.write(arr_str)
            print('Saved output to', csv_file)
except IOError:
    print("I/O error")
