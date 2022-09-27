import pandas as pd
import streamlit as st
from datetime import date
from data.ids import leagues_id

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

st.markdown("""---""")

# Part responsible for the rounds odds visualizer

st.sidebar.header('Round Standing Selector')
comp = st.sidebar.selectbox('Leagues : ', leagues, index=4, key='rounds')

@st.cache
def load_round_odds(comp: str) -> tuple[pd.DataFrame, int]:
    dataf = pd.read_csv(f'./src/rounds/{season}_{comp}.csv', index_col=False)
    return dataf, dataf['Round'].iat[-1]

odds_data, max_round = load_round_odds(comp)

st.header(f"""Displaying Round Odds of *{comp}* """)

round = st.selectbox('Round Number:', list(range(1, max_round + 1)) + ['All'], index=int(max_round))
if round != 'All':
    odds_data = odds_data[odds_data['Round']== round]

teams = pd.read_csv(f'./src/standings/{season}_{comp}_standings.csv', index_col=False)['Name']
team = st.selectbox('Team search:', list(teams) + ['All'], index=len(teams))
if team != 'All':
    odds_data = odds_data.loc[(odds_data['Home'] == team) | (odds_data['Away'] == team)]

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

st.dataframe(odds_data_styled)