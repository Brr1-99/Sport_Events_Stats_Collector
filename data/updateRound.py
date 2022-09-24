import os
from datetime import date, timedelta
from data.loadData import getRoundStats
from .ids import leagues_id

today = date.today()

season = today.year

endRound = today - timedelta(1)

startRound = today - timedelta(4)

ids = leagues_id

def updateRound() -> None:
    for key, value in ids.items():
        df = getRoundStats(value, season, startRound, endRound)
        if not os.path.exists(f'src/rounds/{season}_{key}.csv'):
            df.to_csv(f'src/rounds/{season}_{key}.csv', mode='w', index=False, header=True)
        else:
            df.to_csv(f'src/rounds/{season}_{key}.csv', mode='a', index=False, header=False)
