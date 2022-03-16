# Compile CSV with 'Team1ID', 'Team2ID', and 'Outcome' columns, where the assignment of the first or second team
# has nothing to do with who won. 'Outcome' indicates whether Team1 won (bool).
# We drop results from before 2003 since we have no team data for back then.

import pandas as pd
import random

RESULT_DATA_URL = 'data/MDataFiles_Stage2/MRegularSeasonCompactResults.csv'
OUTPUT_URL = 'allResults.csv'

result_data = pd.read_csv(RESULT_DATA_URL)

trimmed_res_data = result_data.drop(['DayNum', 'WLoc', 'NumOT'], axis=1)
trimmed_res_data = trimmed_res_data.loc[trimmed_res_data['Season'] > 2002]
randomized_res_data = []
for row in trimmed_res_data.itertuples():
    r = random.random()
    if r > .5:
        randomized_res_data.append({'Team1ID': str(row.WTeamID)+'_'+str(row.Season), 'Team2ID': str(row.LTeamID)+'_'+str(row.Season), 'Outcome': True})
    else:
        randomized_res_data.append({'Team1ID': str(row.LTeamID)+'_'+str(row.Season), 'Team2ID': str(row.WTeamID)+'_'+str(row.Season), 'Outcome': False})

res_data = pd.DataFrame(randomized_res_data)
res_data.to_csv(path_or_buf=OUTPUT_URL, index=None)
