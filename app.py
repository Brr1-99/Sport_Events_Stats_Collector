import pandas as pd
import streamlit as st
from datetime import date
from data.updateFuture import update_Future
from data.ids import leagues_id, teams_id

today = date.today()

season = today.year

st.title('Sports Stats Visualizer')

st.markdown("""
This app performs simple request to the API-FOOTBALL Api, provided by RapidAPI. Then it creates a data visualizer using pandas.
* **Python libraries:** [Pandas](https://pandas.pydata.org/), [Streamlit](https://streamlit.io/), [Requests](https://requests.readthedocs.io/en/latest/)
* **Data source:** [RapidAPI](https://rapidapi.com/api-sports/api/api-football/)
""")

leagues = [league for league in leagues_id.keys()]

# Part responsible for the standings visualizer

st.sidebar.header('League Standing Selector')
competition = st.sidebar.selectbox('Leagues : ', leagues, index=4, key='standings')

@st.cache
def load_data(competition: str) -> pd.DataFrame:
    df = pd.read_csv(f'./src/standings/{season}_{competition}_standings.csv', index_col=False)
    return df

standings_data = load_data(competition)
standings_data_styled = standings_data.style\
    .format(precision= 2)\
    .highlight_max(subset=standings_data.columns[4:], color='green', axis=0)

st.header(f"""Displaying Standings of *{competition}* """)
st.dataframe(standings_data_styled)

translate_options = {
    'For Goals': 'FG',
    'Against Goals': 'AG',
    'Goal Diff': 'GD',
    'Wins': 'W',
    'Draws': 'D',
    'Loses': 'L',
}

teams = [team for team in standings_data['Name']]
teams_compare = st.multiselect(
    'Do you want to compare any teams? 🆚',
    teams)

data_teams = standings_data.loc[standings_data['Name'].isin(teams_compare)]

if len(teams_compare) > 1:
    option = st.selectbox('Compare value:', ['For Goals', 'Against Goals', 'Goal Diff', 'Wins', 'Draws', 'Loses', 'All points %','Home points %','Away points %'], index=2)
    st.bar_chart(data_teams, x='Name', y=f'{translate_options[option] if option in translate_options.keys() else option}')

# Function to compute the logo of the team
def logo(name: str) -> str:
    id = teams_id[name]
    return(f"<img src='https://media.api-sports.io/football/teams/{id}.png"
        f"""' style='display:block;margin-left:auto;margin-right:auto;width:40px;border:0;'><div style='text-align:center'>{name}"""
         "</div>")

@st.cache
def load_next_matches(comp: str) -> pd.DataFrame:
    data = update_Future(comp)
    data['Home'] = data['Home'].apply(lambda x: logo(x))
    data['Away'] = data['Away'].apply(lambda x: logo(x))
    return data

data = load_next_matches(competition)

st.header(f"""Displaying next 10 matches for *{competition}* """)
st.write(data.to_html(escape=False, index=False, justify='center'), unsafe_allow_html=True)
st.markdown("""---""")

# Part responsible for the rounds odds visualizer

st.sidebar.header('Round Standing Selector')
comp = st.sidebar.selectbox('Leagues : ', leagues, index=0, key='rounds')

@st.cache
def load_round_odds(comp: str) -> tuple[pd.DataFrame, int]:
    dataf = pd.read_csv(f'./src/rounds/{season}_{comp}.csv', index_col=False)
    return dataf, dataf['Round'].iat[-1]

odds_data, max_round = load_round_odds(comp)

st.header(f"""Displaying Round Odds of *{comp}* """)

round_option, team_option = st.columns(2)

with round_option:
    round = st.selectbox('Round Number:', list(range(1, int(max_round) + 1)) + ['All'], index=int(max_round))
    if round != 'All':
        odds_data = odds_data[odds_data['Round'] == round]
with team_option:
    teams = pd.read_csv(f'./src/standings/{season}_{comp}_standings.csv', index_col=False)['Name']
    team = st.selectbox('Team search:', list(teams) + ['All'], index=len(teams))
    if team != 'All':
        odds_data = odds_data.loc[(odds_data['Home'] == team) | (odds_data['Away'] == team)]

goals_option, number_goals = st.columns(2)

with goals_option:
    goals = st.radio(
    "Over/Under Selection:",
    ('+=', '-='))

with number_goals:
    number = st.selectbox(label='Number of goals ⚽:',options=range(11))
    if goals == '+=':
        odds_data = odds_data.loc[(odds_data['HG'] + odds_data['AG'] >= number)]
    else:
        odds_data = odds_data.loc[(odds_data['HG'] + odds_data['AG'] <= number)]

def show_results(row: object) -> list :
    text = []
    idx = {'1': 0, 'X': 1, '2': 2}
    for item in row:
        if isinstance(item,float):
            text.append('color: red')
        else:
            text.append('')
    text[idx[row['Final']]] = 'color: green'
    text[-2] = 'color: green' if row['Awaited'] == row[row['Final']] else 'color: red'
    return text

odds_data_styled = odds_data.style\
    .format(precision= 2)\
    .apply(show_results, subset=odds_data.columns[4:], axis=1)\
    .highlight_max(subset=odds_data.columns[4:-1], color='blue')

try:
    st.dataframe(odds_data_styled)
except ValueError:
    st.write('No coincidences found ❌. Try with a different value 🤔',)