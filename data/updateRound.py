import os
import pandas as pd
from datetime import date, timedelta
from data.loadData import getRoundStats
from .ids import leagues_id

today = date.today()
season = today.year
endRound = today - timedelta(1)
startRound = today - timedelta(7)
ids = leagues_id

def updateRound() -> None:
    for key, value in ids.items():
        df = getRoundStats(value, season, startRound, endRound)
        if not os.path.exists(f'src/rounds/{season}_{key}.csv'):
            df.to_csv(f'src/rounds/{season}_{key}.csv', mode='w', index=False, header=True)
        else:
            data = pd.read_csv(f'src/rounds/{season}_{key}.csv', index_col=False)
            new_data = pd.concat([data,df])
            new_data.to_csv(f'src/rounds/{season}_{key}.csv', mode='w', index=False, header=True)
