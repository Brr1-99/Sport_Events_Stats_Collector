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

st.sidebar.header('Leagues available')
competition = st.sidebar.selectbox('Leagues : ', leagues)

# @st.cache
# def load_data(option: str, competition: str) -> tuple[pd.DataFrame, int]:
#     df = pd.read_csv(f'./src/rounds/{season}_{competition}.csv', index_col=False)
#     df['1'] = df['1'].apply('{:0>3}'.format)
#     df['X'] = df['X'].apply('{:0>3}'.format)
#     df['2'] = df['2'].apply('{:0>3}'.format)
#     df['Expected'] = df['Expected'].apply('{:0>3}'.format)

#     return df, len(df)

@st.cache
def load_data(competition: str) -> tuple[pd.DataFrame, int]:
    df = pd.read_csv(f'./src/standings/{season}_{competition}_standings.csv', index_col=False)
    df['All points %'] = df['All points %'].apply('{:0>3}'.format)
    df['Home points %'] = df['Home points %'].apply('{:0>3}'.format)
    df['Away points %'] = df['Away points %'].apply('{:0>3}'.format)
    df['W %'] = df['W %'].apply('{:0>3}'.format)
    df['D %'] = df['D %'].apply('{:0>3}'.format)
    df['L %'] = df['L %'].apply('{:0>3}'.format)
    return df, len(df)

data, max = load_data(competition)

data = data.style.highlight_max(subset=data.columns[4:], color='green', axis=0)

st.header(f"""Displaying Standings of *{competition}* """)
st.dataframe(data)
