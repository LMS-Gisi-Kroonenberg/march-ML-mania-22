# Again, we didn't have some teams in out team stats file, but we only miss out on 201 games because of this.

import pandas as pd

TEAM_DATA_URL = 'all_reg_season_team_stats.csv'
RESULT_DATA_URL = 'allResults.csv'
OUTPUT_URL = 'training_data.csv'

team_data = pd.read_csv(TEAM_DATA_URL, index_col=0).drop('Games', axis=1)
result_data = pd.read_csv(RESULT_DATA_URL)

# Create training dataset. The features are the difference of two team's stats,
# team1-team2, and the target is the outcome, whether team1 won.
train = []
for row in result_data.itertuples():
    try:
        stat_diffs = team_data.loc[row.Team1ID] - team_data.loc[row.Team2ID]
    except KeyError:
        continue

    temp_d = dict(zip(list(stat_diffs.index), list(stat_diffs)))
    temp_d['Outcome'] = row.Outcome
    train.append(temp_d)

train_df = pd.DataFrame(train)
train_df.to_csv(path_or_buf=OUTPUT_URL, index=None)
