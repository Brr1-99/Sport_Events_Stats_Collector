import os
import pandas as pd
from datetime import date, timedelta
from data.loadData import getNextGames
from .ids import leagues_id

timelapse = date.today - timedelta(1)
ids = leagues_id

def updateFuture(comp: str) -> pd.DataFrame:
    if timelapse > os.path.getmtime(f'src/future/{comp}.csv') or not os.path.exists(f'src/future/{comp}.csv'):
        df = getNextGames(ids[comp])
        df.to_csv(f'src/future/{comp}.csv', mode='w', index=False, header=True)
    return pd.read_csv(f'src/future/{comp}.csv', index_col=False)
