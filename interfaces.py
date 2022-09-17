# ┌────────────────────────
# │       INTERFACES
# └────────────────────────


# Function to create the match information 
def buildMatch(
    home: str,
    away: str,
    homeOdds: int,
    drawOdds: int,
    awayOdds: int,
    homeGoals: int,
    awayGoals: int,
    ) -> dict:
    return {
        'Home': home,
        'Away': away,
        '1': homeOdds,
        'x': drawOdds,
        '2': awayOdds,
        'HomeGoals': homeGoals,
        'AwayGoals': awayGoals,
    }
