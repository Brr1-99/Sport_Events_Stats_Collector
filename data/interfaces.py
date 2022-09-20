from datetime import datetime

# ┌────────────────────────
# │       INTERFACES
# └────────────────────────

# Function to create the match information 
def buildMatch(
    home: str,
    away: str,
    round: int,
    date: datetime,
    homeOdds: int,
    drawOdds: int,
    awayOdds: int,
    homeGoals: int,
    awayGoals: int,
    ) -> dict:
    return {
        'Home': home,
        'Away': away,
        'Round': round,
        'Date': date,
        '1': homeOdds,
        'X': drawOdds,
        '2': awayOdds,
        'HomeGoals': homeGoals,
        'AwayGoals': awayGoals,
        'Expected': min(homeOdds, drawOdds, awayOdds),
        'Result': getResult(homeGoals, awayGoals)
    }

# Function to compute the match result 
def getResult(homeGoals, awayGoals) -> str:
    if homeGoals > awayGoals:
        return '1'
    if homeGoals < awayGoals:
        return '2'
    return 'X'

# Function to create the team information 
def buildTeam(
    name: str,
    rank: int,
    points: int,
    forGoals: int,
    againstGoals: int,
    goalDiff: int,
    games: int,
    wins: int,
    draws: int, 
    loses: int,
    ) -> dict:
    return {
        'Name': name,
        'Rank': rank,
        'Points': points, 
        'GD': goalDiff,
        'FG': forGoals,
        'AG': againstGoals,
        'W': wins,
        'D': draws,
        'L': loses,
        'Points %': '{:2.f}'.format(100*(points)/games)
    }