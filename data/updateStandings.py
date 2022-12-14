from datetime import date
from data.loadData import get_standings
from .ids import leagues_id

today = date.today()

season = today.year

ids = leagues_id

def update_standings() -> None:
    for key, value in ids.items():
        df = get_standings(value, season)
        df.to_csv(f'src/standings/{season}_{key}_standings.csv', mode='w', index=False, header=True)