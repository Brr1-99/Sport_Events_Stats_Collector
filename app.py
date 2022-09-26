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

st.sidebar.header('League Standing Selector')
competition = st.sidebar.selectbox('Leagues : ', leagues, index=4, key='standings')

@st.cache
def load_data(competition: str) -> pd.DataFrame:
    df = pd.read_csv(f'./src/standings/{season}_{competition}_standings.csv', index_col=False)
    df['All points %'] = df['All points %'].apply('{:0>3}'.format)
    df['Home points %'] = df['Home points %'].apply('{:0>3}'.format)
    df['Away points %'] = df['Away points %'].apply('{:0>3}'.format)
    df['W %'] = df['W %'].apply('{:0>3}'.format)
    df['D %'] = df['D %'].apply('{:0>3}'.format)
    df['L %'] = df['L %'].apply('{:0>3}'.format)
    return df

standings_data = load_data(competition)
standings_data = standings_data.style.highlight_max(subset=standings_data.columns[4:], color='green', axis=0)

st.header(f"""Displaying Standings of *{competition}* """)
st.dataframe(standings_data)

st.markdown("""---""")

st.sidebar.header('Round Standing Selector')
comp = st.sidebar.selectbox('Leagues : ', leagues, index=4, key='rounds')

@st.cache
def load_round_odds(comp: str) -> tuple[pd.DataFrame, int]:
    dataf = pd.read_csv(f'./src/rounds/{season}_{comp}.csv', index_col=False)
    dataf['1'] = dataf['1'].apply('{:0>3}'.format)
    dataf['X'] = dataf['X'].apply('{:0>3}'.format)
    dataf['2'] = dataf['2'].apply('{:0>3}'.format)
    dataf['Awaited'] = dataf['Awaited'].apply('{:0>3}'.format)

    return dataf, dataf['Round'].iat[-1]

odds_data, max_round = load_round_odds(comp)

st.header(f"""Displaying Round Odds of *{comp}* """)

round = st.selectbox('Round Number:', list(range(1,max_round+1))+['All'], index=int(max_round))
if round != 'All':
    odds_data = odds_data[odds_data['Round']== round]

teams = pd.read_csv(f'./src/standings/{season}_{comp}_standings.csv', index_col=False)['Name']
team = st.selectbox('Team search:', list(teams) + ['All'], index=len(teams))
if team != 'All':
    odds_data = odds_data.loc[(odds_data['Home']== team) | (odds_data['Away'] == team)]

odds_data = odds_data.style.highlight_max(subset=odds_data.columns[4:], color='green', axis=0)

st.dataframe(odds_data)
