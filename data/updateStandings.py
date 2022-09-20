import os
from datetime import date, timedelta
from data.loadData import getRoundStats
from ids import leagues_id

today = date.today()

season = today.year

endRound = today - timedelta(1)

startRound = today - timedelta(4)

ids = leagues_id

for key, value in ids.items():
    df = getRoundStats(value, season, startRound, endRound)
    if not os.path.exists(f'../src/standings/{season}_{key}_standings.csv'):
        df.to_csv(f'../src/standings/{season}_{key}_standings.csv', mode='w', index=True, header=True)
    else:
        df.to_csv(f'../src/standings/{season}_{key}_standings.csv', mode='a', index=True, header=False)