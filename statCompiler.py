# Re-written to use dataframes. Also added 'games' column to output CSV.
# I tested the output to make sure it matched the previous for 2003.
#
# There were only eight winless seasons, so getting team ID's via the winning team is okay.
#

import pandas as pd

never_won = []

# Added 'WinPct' (season winning percentage) and 'Games' (games played).
STAT_COLUMNS = csv_columns = ['Score','FGM', 'FGA', 'FGM3', 'FGA3', 'FTM', 'FTA', 'OR', 'DR', 'AST', 'TO', 'STL', 'BLK', 'PF', 'WinPct', 'Games']

url = 'data/MDataFiles_Stage2/MRegularSeasonDetailedResults.csv'
dataset = pd.read_csv(url)  # By default, dataframe has csv's first row as column names.

# Add WTeamSeasonID column -- a teamSeasonID is a team w/ season -- formatted 'TeamID_season', for example '1242_2008'.
dataset['WTeamSeasonID'] = dataset.apply(lambda row: str(row.WTeamID) + '_' + str(row.Season), axis=1)
teams = pd.unique(dataset.sort_values('WTeamSeasonID')['WTeamSeasonID'])
team_stats = pd.DataFrame(0, index=teams, columns=STAT_COLUMNS)  # DF for all teams with all zeroes in each stat column.

# Sum each stat over all games.
for game in dataset.itertuples(index=False):
    W_stats = [game[3], game[8], game[9], game[10], game[11], game[12], game[13], game[14], game[15], game[16],
               game[17], game[18], game[19], game[20], 1, 1]
    L_stats = [game[5], game[21], game[22], game[23], game[24], game[25], game[26], game[27], game[28], game[29],
               game[18], game[31], game[32], game[33], 0, 1]

    w_team_season_id = str(game.WTeamID) + '_' + str(game.Season)
    l_team_season_id = str(game.LTeamID) + '_' + str(game.Season)

    try:
        team_stats.loc[w_team_season_id] += W_stats
    except KeyError:
        if w_team_season_id not in never_won:
            never_won.append(w_team_season_id)

    try:
        team_stats.loc[l_team_season_id] += L_stats
    except KeyError:
        if l_team_season_id not in never_won:
            never_won.append(l_team_season_id)

# Divide to get average of stats.
for col in team_stats:
    if col != 'Games':
        team_stats[col] = team_stats.apply(lambda row: row[col] / row['Games'], axis=1)

# Export to csv
csv_file = "all_reg_season_team_stats.csv"
team_stats.to_csv(path_or_buf=csv_file)

print(len(never_won))
print(*never_won)
