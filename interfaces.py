# ┌────────────────────────
# │       INTERFACES
# └────────────────────────


# Function to create the match information 
def buildMatch(
    home: str,
    away: str,
    league: str,
    homeOdds: int,
    drawOdds: int,
    awayOdds: int,
    homeGoals: int,
    awayGoals: int,
    ) -> dict:
    return {
        'home': home,
        'away': away,
        'league': league,
        '1': homeOdds,
        'x': drawOdds,
        '2': awayOdds,
        'homeGoals': homeGoals,
        'awayGoals': awayGoals,
    }
