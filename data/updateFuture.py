import os
import pandas as pd
import datetime
from data.loadData import get_next_games
from .ids import leagues_id

ids = leagues_id

def update_Future(comp: str) -> pd.DataFrame:

    timelapse = datetime.date.today() - datetime.timedelta(1)
    changed = datetime.date.fromtimestamp(os.path.getmtime(f'src/future/{comp}.csv'))

    if timelapse >= changed:
        df = get_next_games(ids[comp])
        df.to_csv(f'src/future/{comp}.csv', mode='w', index=False, header=True)
    return pd.read_csv(f'src/future/{comp}.csv', index_col=False)
