from datetime import datetime
import requests, os
import pandas as pd
from dotenv import load_dotenv
from data.interfaces import buildMatch, buildTeam

load_dotenv()

base_url = "https://api-football-v1.p.rapidapi.com/v3/"

headers = {
        "X-RapidAPI-Key": os.getenv("API_KEY"),
        "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
    }

def getRoundStats(value: int, season: int, startRound: datetime, endRound: datetime) -> pd.DataFrame:

    querystring = {"league":f"{value}","season":f"{season}","from":f"{startRound}","to":f"{endRound}","timezone":"Europe/Madrid", "status":"NS-FT"}

    response = requests.request("GET", base_url + 'fixtures', headers=headers, params=querystring).json()
    num_round = response['response'][0]['league']['round'].split(' ')[-1]

    matchs = []

    for item in response['response']:

        id = item['fixture']['id']
        datetime = item['fixture']['date'].split('T')[0]

        date = datetime.split('-')[-1] + datetime.split('-')[-2]

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
            home=homeTeam, away=awayTeam, round=num_round, date=date,
            homeOdds=homeTeamOdds, drawOdds=drawOdds, awayOdds=awayTeamOdds, 
            homeGoals=homeGoals, awayGoals=awayGoals
            ))

    return pd.DataFrame.from_records(matchs)


def obtainYield(stand: dict, param: str) -> int:

    games = stand[f'{param}']['played']
    wins = stand[f'{param}']['win']
    draws = stand[f'{param}']['draw']

    return (100 * (wins + draws/3) / games)

def getStandings(leagueId: int, season: int) -> pd.DataFrame:

    querystring = {"season":f"{season}","league": f"{leagueId}"} 

    response = requests.request("GET", base_url + 'standings', headers=headers, params=querystring).json()

    standings = response['response'][0]['league']['standings'][0]

    teams = []

    for stand in standings:

        rank = stand['rank']
        name = stand['team']['name']
        points = stand['points']
        form = stand['form']

        forGoals = stand['all']['goals']['for']
        againstGoals = stand['all']['goals']['against']
        goalDiff = stand['goalsDiff']

        totalGames = stand['all']['played']
        totalWins = stand['all']['win']
        totalDraws = stand['all']['draw']
        totalLoses = stand['all']['lose']

        allPoints = obtainYield(stand, 'all')
        homePoints = obtainYield(stand, 'home')
        awayPoints = obtainYield(stand, 'away')

        teams.append(buildTeam(
            name=name, rank=rank, points=points, form=form,
            forGoals=forGoals, againstGoals=againstGoals, goalDiff=goalDiff,
            games=totalGames, wins=totalWins, draws=totalDraws, loses=totalLoses,
            allPoints=allPoints, homePoints=homePoints, awayPoints=awayPoints,
        ))
    
    return pd.DataFrame.from_records(teams)