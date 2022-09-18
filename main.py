from datetime import date, timedelta
from loadData import getValues

today = date.today()

season = today.year

endRound = today - timedelta(1)

startRound = today - timedelta(4)

leagues_id = {
    "Premier_League": 39,
    "Ligue_1": 61,
    "Bundesliga": 78,
    "Serie_A": 135,
    "La_Liga" : 140,
}

for key, value in leagues_id.items():
	df = getValues(value, season, startRound, endRound)
	print(df)