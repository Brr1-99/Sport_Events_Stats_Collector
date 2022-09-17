import requests, os
import pandas as pd
from datetime import date, timedelta
from dotenv import load_dotenv
from interfaces import buildMatch

load_dotenv()

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

base_url = "https://api-football-v1.p.rapidapi.com/v3/"

querystring = {"league":"140","season":f"{season}","from":f"{startRound}","to":f"{endRound}","timezone":"Europe/Madrid", "status":"NS-FT"}

headers = {
	"X-RapidAPI-Key": os.getenv("API_KEY"),
	"X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
}

response = requests.request("GET", base_url + 'fixtures', headers=headers, params=querystring).json()


round = response['response'][0]['league']['round']
leagueName = response['response'][0]['league']['name']

matchs = []

for item in response['response']:

	id = item['fixture']['id']

	homeTeam = item['teams']['home']['name']
	awayTeam = item['teams']['away']['name']

	homeGoals = item['goals']['home']
	awayGoals = item['goals']['away']

	oddsquerystring = {"fixture":f"{id}","league":"140","season":f"{season}","timezone":"Europe/Madrid","bookmaker":"8","bet":"1"}

	oddsresponse = requests.request("GET", base_url + 'odds', headers=headers, params=oddsquerystring).json()

	values = oddsresponse['response'][0]['bookmakers'][0]['bets'][0]['values']

	homeTeamOdds = values[0]['odd']
	drawOdds = values[1]['odd']
	awayTeamOdds = values[2]['odd']

	expected = min(homeTeamOdds, drawOdds, awayTeamOdds)

	matchs.append(buildMatch(
		home=homeTeam, away=awayTeam, 
		homeOdds=homeTeamOdds, drawOdds=drawOdds, awayOdds=awayTeamOdds, 
		homeGoals=homeGoals, awayGoals=awayGoals
		))

df = pd.DataFrame.from_records(matchs)

print(df)