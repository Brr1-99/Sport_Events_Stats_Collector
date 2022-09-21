import os
from datetime import date, timedelta
from data.loadData import getStandings
from .ids import leagues_id

today = date.today()

season = today.year

endRound = today - timedelta(1)

startRound = today - timedelta(4)

ids = leagues_id

def updateStandings() -> None:
    for key, value in ids.items():
        df = getStandings(value, season)
        df.to_csv(f'src/standings/{season}_{key}_standings.csv', mode='w', index=False, header=True)