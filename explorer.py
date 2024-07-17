import streamlit as st
from lib.helpers import line_per_cat, format_number
from eldar import Query
import pandas as pd





df =  st.session_state['df']
df_filter =  st.session_state['df_filter']

date = st.session_state['date']
txt_query = st.session_state['txt_query']
ignore_case = st.session_state['ignore_case']
ignore_accent = st.session_state['ignore_accent']
match_word = st.session_state['match_word']
plateforme_color_palette = st.session_state['plateforme_color_palette']
rolling_period = st.session_state['rolling_period']
rolling_periods = st.session_state['rolling_period_values']   
rolling_period = rolling_periods.get(rolling_period)

rolling_period = st.sidebar.selectbox("Rolling period", ['1D','7D','1ME'], index = 0)
sort_by = st.sidebar.selectbox("Sort by", ["engagements", "views"], index=0)
nb_verbatims = st.sidebar.number_input("Number of verbatims",value = 150)

df_twitter = df_filter[df_filter['plateforme']=="Twitter"].reset_index(drop=True)
df_telegram = df_filter[df_filter['plateforme']=="Telegram"].reset_index(drop=True)

###############################################
# DATA FILTERING
###############################################
total_posts_telegram = df[df['plateforme']=='Telegram']['message_id'].nunique()
total_channels_telegram = df[df['plateforme']=='Telegram']['user_id'].nunique()
sum_views_telegram = df[df['plateforme']=='Telegram']['views'].sum()
sum_eng_telegram = df[df['plateforme']=='Telegram']['engagements'].sum()

total_posts_twitter = df[df['plateforme']=='Twitter']['message_id'].nunique()
total_channels_twitter = df[df['plateforme']=='Twitter']['user_id'].nunique()
sum_views_twitter = df[df['plateforme']=='Twitter']['views'].sum()
sum_eng_twitter = df[df['plateforme']=='Twitter']['engagements'].sum()

################################################
# DATA PREP
################################################
metrics = {
'posts' : ('message_id',"nunique"),
'views': ('views', 'sum'),
'engagements': ('engagements', 'sum'),
'share': ('share', 'sum'),
'likes': ('likes', 'sum'),
'comments': ('comments', 'sum')
}

df_filter["datetime"]= pd.to_datetime(df_filter["date"])
df_filter.set_index('datetime', inplace=True)
df_filter = df_filter.groupby("plateforme").resample(rolling_period).agg(**metrics).reset_index()
df_filter["datetime"]=df_filter["datetime"].dt.strftime("%Y-%m-%d")
df_filter['color'] = df_filter['plateforme'].map(plateforme_color_palette)

###############################################
# KEY METRICS
###############################################

# fig = px.line(df_trends_channels, x='datetime', y='posts', color='plateforme')
if len(df_filter)>0:
    fig = line_per_cat(df_filter, "datetime", "posts", "plateforme", plateforme_color_palette, xaxis_title="Date", yaxis_title="Posts", title_text="Posts per day", col_hover=["views", "engagements", "share", "likes", "comments"], height=500)
    st.plotly_chart(fig, use_container_width=True, theme="streamlit")
else : 
    st.write("NO DATA")

col1, col2 = st.columns(2, gap="medium")

with col1:
    st.header("Telegram", divider="green")
    sub_col1, sub_col2, sub_col3, sub_col4 = st.columns(4, gap="small")

    with sub_col1:
        st.markdown(f'<div class="card"><div class="card-body"><div class="row align-items-center"><div class="col"><h7 class="card-title text-uppercase text-muted mb-2">Verbatims</h7><div class ="h2 mb-0">{format_number(df_telegram["message_id"].nunique())}</div></div></div></div></div>', unsafe_allow_html= True)
    with sub_col2:
        card = f'<div class="card"><div class="card-body"><div class="row align-items-center"><div class="col"><h7 class="card-title text-uppercase text-muted mb-2">Channels</h7><div class ="h2 mb-0">{format_number(df_telegram["user_id"].nunique())}</div></div></div></div></div>'
        st.markdown(card, unsafe_allow_html= True)
    with sub_col3:
        card = f'<div class="card"><div class="card-body"><div class="row align-items-center"><div class="col"><h7 class="card-title text-uppercase text-muted mb-2">Views</h7><div class ="h2 mb-0">{format_number(df_telegram["views"].nunique())}</div></div></div></div></div>'
        st.markdown(card, unsafe_allow_html= True)  
    with sub_col4:
        card = f'<div class="card"><div class="card-body"><div class="row align-items-center"><div class="col"><h8 class="card-title text-uppercase text-muted mb-2">Engagements</h8><div class ="h2 mb-0">{format_number(df_telegram["engagements"].nunique())}</div></div></div></div></div>'
        st.markdown(card, unsafe_allow_html= True)
    st.markdown("<hr>", unsafe_allow_html= True)
    if len(df_telegram)>0:
        for i, row in df_telegram.sort_values(by=sort_by, ascending=False).head(nb_verbatims).iterrows():
            card=f'<div class="card"><div class="card-header bg-success bg-opacity-25 d-flex justify-content-between"><h5 class="p-2"><span style=" display: inline-block;width: 30px;height: 30px;background-color: #b1b1b1;  color: white;border-radius: 50%; text-align: center;line-height: 30px;font-size: 16px;margin-right: 10px;font-weight: bold;">{row["user_name"][0]}</span><b>{row["user_name"]}</b></h5><div class="p-2"></div><div class="p-2"><i class="fa-regular fa-clock fa-xs"></i> {row["date"].strftime("%d/%m/%y")}</div></div><div class="card-body"><p class="card-text">{row["translated_text"]}</p></div><div class="card-footer d-flex justify-content-between"><div class="p-2"><i class="fa-solid fa-chart-column fa-xs"></i> {format_number(row["engagements"])}</div><div class="p-2"><i class="fa-regular fa-eye fa-xs"></i> {format_number(row["views"])}</div><div class="p-2"><i class="fa-solid fa-retweet fa-xs"></i> {format_number(row["share"])}</div><div class="p-2"><i class="fas fa-heart  fa-xs"></i> {format_number(row["likes"])}</div><div class="p-2"><i class="fas fa-comments fa-xs"></i> {format_number(row["comments"])}</div></div></div><br/>'
            st.markdown(card, unsafe_allow_html= True)
    else:
        st.write("NO DATA")
with col2:
    st.header("Twitter", divider="blue")
    t_sub_col1, t_sub_col2, t_sub_col3, t_sub_col4 = st.columns(4, gap="small")

    with t_sub_col1:
        st.markdown(f'<div class="card"><div class="card-body"><div class="row align-items-center"><div class="col"><h7 class="card-title text-uppercase text-muted mb-2">Verbatims</h7><div class ="h2 mb-0">{format_number(df_twitter["message_id"].nunique())}</div></div></div></div></div>', unsafe_allow_html= True)
    with t_sub_col2:
        card = f'<div class="card"><div class="card-body"><div class="row align-items-center"><div class="col"><h7 class="card-title text-uppercase text-muted mb-2">Channels</h7><div class ="h2 mb-0">{format_number(df_twitter["user_id"].nunique())}</div></div></div></div></div>'
        st.markdown(card, unsafe_allow_html= True)
    with t_sub_col3:
        card = f'<div class="card"><div class="card-body"><div class="row align-items-center"><div class="col"><h7 class="card-title text-uppercase text-muted mb-2">Views</h7><div class ="h2 mb-0">{format_number(df_twitter["views"].nunique())}</div></div></div></div></div>'
        st.markdown(card, unsafe_allow_html= True)
    with t_sub_col4:
        card = f'<div class="card"><div class="card-body"><div class="row align-items-center"><div class="col"><h8 class="card-title text-uppercase text-muted mb-2">Engagements</h8><div class ="h2 mb-0">{format_number(df_twitter["engagements"].nunique())}</div></div></div></div></div>'
        st.markdown(card, unsafe_allow_html= True)
    st.markdown("<hr>", unsafe_allow_html= True)
    if len(df_twitter)>0:
        for i, row in df_twitter.sort_values(by=sort_by, ascending=False).head(nb_verbatims).iterrows():
            card=f'<div class="card"><div class="card-header bg-info bg-opacity-25 d-flex justify-content-between"><h5 class="p-2"><span style=" display: inline-block;width: 30px;height: 30px;background-color: #0099EF;  color: white;border-radius: 50%; text-align: center;line-height: 30px;font-size: 16px;margin-right: 10px;font-weight: bold;">{row["user_name"][0]}</span><b>{row["user_name"]}</b></h5><div class="p-2"></div><div class="p-2"><i class="fa-regular fa-clock fa-xs"></i> <a href="https://www.twitter.com/{row["user_name"]}/status/{row["message_id"]}">{row["date"].strftime("%d/%m/%y")}</a></div></div><div class="card-body"><p class="card-text">{row["translated_text"]}</p></div><div class="card-footer d-flex justify-content-between"><div class="p-2"><i class="fa-solid fa-chart-column fa-xs"></i> {format_number(row["engagements"])}</div><div class="p-2"><i class="fa-regular fa-eye fa-xs"></i> {format_number(row["views"])}</div><div class="p-2"><i class="fa-solid fa-retweet fa-xs"></i> {format_number(row["share"])}</div><div class="p-2"><i class="fas fa-heart  fa-xs"></i> {format_number(row["likes"])}</div><div class="p-2"><i class="fas fa-comments fa-xs"></i> {format_number(row["comments"])}</div></div></div><br/>'
            st.markdown(card, unsafe_allow_html= True)
    else:
        st.write("NO DATA")