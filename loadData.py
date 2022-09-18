from datetime import datetime
import requests, os
import pandas as pd
from dotenv import load_dotenv
from interfaces import buildMatch

load_dotenv()

base_url = "https://api-football-v1.p.rapidapi.com/v3/"

def getValues(value: int, season: int, startRound: datetime, endRound: datetime) -> pd.DataFrame:

    querystring = {"league":f"{value}","season":f"{season}","from":f"{startRound}","to":f"{endRound}","timezone":"Europe/Madrid", "status":"NS-FT"}

    headers = {
        "X-RapidAPI-Key": os.getenv("API_KEY"),
        "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
    }

    response = requests.request("GET", base_url + 'fixtures', headers=headers, params=querystring).json()

    round = response['response'][0]['league']['round']

    matchs = []

    for item in response['response']:

        id = item['fixture']['id']
        date = item['fixture']['date'].split('T')[0]

        homeTeam = item['teams']['home']['name']
        awayTeam = item['teams']['away']['name']

        homeGoals = item['goals']['home']
        awayGoals = item['goals']['away']

        oddsquerystring = {"fixture":f"{id}","league":f"{value}","season":f"{season}","timezone":"Europe/Madrid","bookmaker":"8","bet":"1"}

        oddsresponse = requests.request("GET", base_url + 'odds', headers=headers, params=oddsquerystring).json()

        values = oddsresponse['response'][0]['bookmakers'][0]['bets'][0]['values']

        homeTeamOdds = values[0]['odd']
        drawOdds = values[1]['odd']
        awayTeamOdds = values[2]['odd']

        matchs.append(buildMatch(
            home=homeTeam, away=awayTeam, round=round, date=date,
            homeOdds=homeTeamOdds, drawOdds=drawOdds, awayOdds=awayTeamOdds, 
            homeGoals=homeGoals, awayGoals=awayGoals
            ))

    return pd.DataFrame.from_records(matchs)
