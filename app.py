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
option = st.sidebar.selectbox('Stats from : ', ['Winrate', 'Goals'])
highlight = st.sidebar.selectbox('Highlighted values : ', ['None', 'Max', 'Min'])

@st.cache
def load_data(option: str, competition: str) -> tuple[pd.DataFrame, int]:
    df = pd.read_csv(f'./src/rounds/{season}_{competition}.csv', index_col=False)
    df['1'] = df['1'].apply('{:0>3}'.format)
    df['X'] = df['X'].apply('{:0>3}'.format)
    df['2'] = df['2'].apply('{:0>3}'.format)
    df['Expected'] = df['Expected'].apply('{:0>3}'.format)

    return df, len(df)

data, max = load_data(option, competition)

limit = st.slider(label= 'Number of data to show', max_value=max, min_value=1, value=int(max/2))

data = data[:limit].style.highlight_max(axis=0, color="green")

st.header(f"""Displaying *{option}* Stats of *{competition}* """)
st.dataframe(data)
