import streamlit as st
from opsci_toolbox.helpers.common import read_json, load_pickle, load_parquet
from datetime import datetime
from lib.helpers import update_session_state
import pandas as pd
from eldar import Query

@st.cache_data 
def load_data(path):
    df = load_pickle(path)
    df['user_name'] = df['user_name'].fillna("NA").astype(str)
    df["datetime"] = df['date'].dt.date  
    return df

def main():
    st.set_page_config(page_title="Data manager", page_icon=":material/edit:", layout="wide",initial_sidebar_state="expanded",)

    st.markdown("""<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
                <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz" crossorigin="anonymous"></script>
                """,unsafe_allow_html=True)
    
    st.write('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.2.0/css/all.min.css"/>', unsafe_allow_html=True)

    explorer_page = st.Page("explorer.py", title="Explorer", icon="👓")
    topics_page = st.Page("topics.py", title="Topics", icon="🚀")
    entities_page = st.Page("entities.py", title="Entities", icon="🗽")
    user_analytics_page = st.Page("users_analytics.py", title="Top Users", icon="🗣️")
    domains_page = st.Page("domains.py", title="Top URLS", icon="🌎")

    pg = st.navigation([explorer_page, topics_page, entities_page,user_analytics_page, domains_page])
   
    df = load_data("data/20240717_df_light.pickle")


    plateforme_color_palette = read_json("data/plateforme_color_palette.json")
    ###############################################
    # SIDEBAR SETTINGS / PARAMETERS
    ###############################################
    if 'df' not in st.session_state:
        st.session_state['df'] = df
    if 'txt_query' not in st.session_state:
        st.session_state['txt_query'] = 'olympics'
    if 'date' not in st.session_state:
        st.session_state['date'] = [df['datetime'].min(), df['datetime'].max()]
    if 'ignore_case' not in st.session_state:
        st.session_state['ignore_case'] = True
    if 'ignore_accent' not in st.session_state:
        st.session_state['ignore_accent'] = True
    if 'match_word' not in st.session_state:
        st.session_state['match_word'] = True
    if 'rolling_period' not in st.session_state:
        st.session_state['rolling_period'] = 0
    if 'rolling_period_values' not in st.session_state:
        st.session_state['rolling_period_values'] = {0: '1D', 1 :'7D', 2 : '1ME'}
    if "plateforme_color_palette" not in st.session_state:
        st.session_state['plateforme_color_palette'] = plateforme_color_palette
        

    # rolling_periods = st.session_state['rolling_period_values']   
    
    txt_query = st.sidebar.text_area("Search using boolean query", value=st.session_state['txt_query'], height=None, max_chars=None, key=None, help=None, on_change=None, args=None, kwargs=None, placeholder=None, disabled=False)
    date = st.sidebar.date_input("Timerange", value = st.session_state['date'], min_value=df['datetime'].min(), max_value=df['datetime'].max())
    ignore_case = st.sidebar.toggle("Ignore case", value=st.session_state['ignore_case'])
    ignore_accent = st.sidebar.toggle("Ignore accent", value=st.session_state['ignore_accent'])
    match_word = st.sidebar.toggle("Match words", value=st.session_state['match_word'])
    # rolling_period = st.sidebar.selectbox("Rolling period", list(rolling_periods.values()), index = st.session_state['rolling_period'])

    
    df = df[(df['datetime'] >= date[0]) & (df['datetime'] <= date[1])]


    df_twitter = df[df['plateforme']=="Twitter"].reset_index(drop=True)
    df_telegram = df[df['plateforme']=="Telegram"].reset_index(drop=True)

    boolean_query = Query(txt_query, ignore_case=ignore_case, ignore_accent=ignore_accent, match_word=match_word)
    df_telegram = df_telegram[df_telegram["translated_text"].apply(boolean_query)]
    df_twitter = df_twitter[df_twitter["translated_text"].apply(boolean_query)]

    df_filter = pd.concat([df_telegram, df_twitter]).reset_index()

    states = {"txt_query" : txt_query, 
              "date" : date, 
              "ignore_case" : ignore_case, 
              "ignore_accent" : ignore_accent, 
              "match_word" : match_word, 
            #   "rolling_period" :  list(rolling_periods.values()).index(rolling_period), 
              "df" : df, 
              "df_filter" : df_filter, 
              "plateforme_color_palette" : plateforme_color_palette,
            #   "rolling_period_values" : rolling_periods
              }
    update_session_state(states)
   
    pg.run()
if __name__ == "__main__":
    main()