from datetime import datetime

# ┌────────────────────────
# │       INTERFACES
# └────────────────────────

# Function to create the finished match information 
def build_match(
    home: str,
    away: str,
    round: int,
    date: datetime,
    homeOdds: int,
    drawOdds: int,
    awayOdds: int,
    homeGoals: int,
    awayGoals: int,
    ) -> dict[str, str | int | datetime]:
    return {
        'Home': home,
        'Away': away,
        'Round': round,
        'Date': date,
        '1': homeOdds,
        'X': drawOdds,
        '2': awayOdds,
        'HG': homeGoals,
        'AG': awayGoals,
        'Awaited': min(homeOdds, drawOdds, awayOdds),
        'Final': get_result(homeGoals, awayGoals),
    }

# Function to create an upcoming match
def build_event(
    homeTeam: str,
    awayTeam: str,
    date: datetime,
    hour: str
    ) -> dict[str, str | datetime]:
    return {
        'Home': homeTeam,
        'Away': awayTeam,
        'Date': date,
        'Hour': hour,
    }

# Function to compute the match result 
def get_result(homeGoals: int, awayGoals: int) -> str:
    if homeGoals > awayGoals:
        return '1'
    if homeGoals < awayGoals:
        return '2'
    return 'X'

# Function to create the team information 
def build_team(
    name: str,
    rank: int,
    points: int,
    form : str,
    forGoals: int,
    againstGoals: int,
    goalDiff: int,
    games: int,
    wins: int,
    draws: int, 
    loses: int,
    allPoints: int,
    homePoints: int,
    awayPoints: int,
    ) -> dict[str, str | int]:
    return {
        'Name': name,
        'Rank': rank,
        'Points': points,
        'Last 5': form, 
        'FG': forGoals,
        'AG': againstGoals,
        'GD': goalDiff,
        'W': wins,
        'D': draws,
        'L': loses,
        'All points %': '{:.2f}'.format(allPoints),
        'Home points %': '{:.2f}'.format(homePoints),
        'Away points %': '{:.2f}'.format(awayPoints),
        'W %': '{:.2f}'.format(100*wins/games),
        'D %': '{:.2f}'.format(100*draws/games),
        'L %': '{:.2f}'.format(100*loses/games),
    }