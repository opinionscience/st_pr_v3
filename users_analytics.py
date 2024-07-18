import streamlit as st
from eldar import Query
import pandas as pd
from lib.helpers import format_number, check_engagement_type

sort_by = st.sidebar.selectbox("Sort by", ["posts", "engagements", "views"], index=0)
nb_users = st.sidebar.number_input("Number of Top Users",value = 10)


date = st.session_state['date']
txt_query = st.session_state['txt_query']
ignore_case = st.session_state['ignore_case']
ignore_accent = st.session_state['ignore_accent']
match_word = st.session_state['match_word']
df = st.session_state['df']
df_filter = st.session_state['df_filter']

# df = df[(df['datetime'] >= date[0]) & (df['datetime'] <= date[1])]


# df_twitter = df[df['plateforme']=="Twitter"].reset_index(drop=True)
# df_telegram = df[df['plateforme']=="Telegram"].reset_index(drop=True)

# boolean_query = Query(txt_query, ignore_case=ignore_case, ignore_accent=ignore_accent, match_word=match_word)
# df_telegram = df_telegram[df_telegram["translated_text"].apply(boolean_query)]
# df_twitter = df_twitter[df_twitter["translated_text"].apply(boolean_query)]

# df_new = pd.concat([df_telegram, df_twitter]).reset_index()

df_twitter = df_filter[df_filter['plateforme']=="Twitter"].reset_index(drop=True)
df_telegram = df_filter[df_filter['plateforme']=="Telegram"].reset_index(drop=True)

metrics = {
'posts' : ('message_id',"nunique"),
'views': ('views', 'sum'),
'engagements': ('engagements', 'sum'),
'share': ('share', 'sum'),
'likes': ('likes', 'sum'),
'comments': ('comments', 'sum')
}

df_users_telegram = df_telegram.groupby(["user_id", 'user_name']).agg(**metrics).reset_index()
df_users_twitter= df_twitter.groupby(["user_id", 'user_name']).agg(**metrics).reset_index()

col1, col2 = st.columns(2, gap="medium")

with col1:
    st.header("Telegram", divider="green")
    if len(df_users_telegram) > 0:
        st.write("<h3>Top Publishers</h3>", unsafe_allow_html=True)
        for i, row in df_users_telegram.sort_values(by=sort_by, ascending=False).head(nb_users).iterrows():
            card=f'<div class="card"><div class="card-header d-flex justify-content-between"><div class="col"><h5 class="p-2"><span style=" display: inline-block;width: 30px;height: 30px;background-color: #0099EF; color: white;border-radius: 50%; text-align: center;line-height: 30px;font-size: 16px;margin-right: 10px;font-weight: bold;">{row["user_name"][0]}</span><b>{row["user_name"]}</b></h5></div><div class="col d-flex justify-content-between"><div class="p-2"><i class="fa-solid fa-message fa-xs"></i> {format_number(row["posts"])}</div><div class="p-2"><i class="fa-solid fa-chart-column fa-xs"></i> {format_number(row["engagements"])}</div><div class="p-2"><i class="fa-regular fa-eye fa-xs"></i> {format_number(row["views"])}</div></div></div></div>'
            st.markdown(card, unsafe_allow_html= True)
            with st.expander("See top messages", icon=":material/chat:"):
                current_messages = df_telegram[df_telegram['user_id'] == row['user_id']].sort_values(by="engagements", ascending=False).head(10)
                for i, msg in current_messages.iterrows():
                    eng_type = check_engagement_type(msg["type_engagement"])
                    msg_card=f'<div class="card"><div class="card-header bg-success bg-opacity-25 d-flex justify-content-between"><h5 class="p-2"><span style=" display: inline-block;width: 30px;height: 30px;background-color: #b1b1b1;  color: white;border-radius: 50%; text-align: center;line-height: 30px;font-size: 16px;margin-right: 10px;font-weight: bold;">{msg["user_name"][0]}</span><b>{msg["user_name"]}</b></h5><div class="p-2"></div><div class="p-2"><i class="fa-regular fa-clock fa-xs"></i> {msg["date"].strftime("%d/%m/%y")}</div></div><div class="card-body"><p class="card-text">{msg["translated_text"]}</p></div><div class="card-footer d-flex justify-content-between">{eng_type}<div class="p-2"><i class="fa-solid fa-chart-column fa-xs"></i> {format_number(msg["engagements"])}</div><div class="p-2"><i class="fa-regular fa-eye fa-xs"></i> {format_number(msg["views"])}</div><div class="p-2"><i class="fa-solid fa-retweet fa-xs"></i> {format_number(msg["share"])}</div><div class="p-2"><i class="fas fa-heart  fa-xs"></i> {format_number(msg["likes"])}</div><div class="p-2"><i class="fas fa-comments fa-xs"></i> {format_number(msg["comments"])}</div></div></div><br/>'
                    st.write(msg_card, unsafe_allow_html= True)
    else:
        st.write("NO DATA")

with col2:
    st.header("Twitter", divider="blue")
    if len(df_users_twitter) > 0:
        st.write("<h3>Top Publishers</h3>", unsafe_allow_html=True)
        for i, row in df_users_twitter.sort_values(by=sort_by, ascending=False).head(nb_users).iterrows():
            card = f'<div class="card"><div class="card-header d-flex justify-content-between"><div class="col"><h5 class="p-2"><span style=" display: inline-block;width: 30px;height: 30px;background-color: #0099EF; color: white;border-radius: 50%; text-align: center;line-height: 30px;font-size: 16px;margin-right: 10px;font-weight: bold;">{row["user_name"][0]}</span><b><a href="https://www.twitter.com/{row["user_name"]}">{row["user_name"]}</a></b></h5></div><div class="col d-flex justify-content-between"><div class="p-2"><i class="fa-solid fa-message fa-xs"></i> {format_number(row["posts"])}</div><div class="p-2"><i class="fa-solid fa-chart-column fa-xs"></i> {format_number(row["engagements"])}</div><div class="p-2"><i class="fa-regular fa-eye fa-xs"></i> {format_number(row["views"])}</div></div></div></div>'
            st.markdown(card, unsafe_allow_html= True)
            with st.expander("See top tweets", icon=":material/chat:"):
                current_tweets = df_twitter[df_twitter['user_id'] == row['user_id']].sort_values(by="engagements", ascending=False).head(10)
                for i, tweet in current_tweets.iterrows():
                    eng_type = check_engagement_type(tweet["type_engagement"])
                    tweet_card=f'<div class="card"><div class="card-header bg-info bg-opacity-25 d-flex justify-content-between"><h5 class="p-2"><span style=" display: inline-block;width: 30px;height: 30px;background-color: #0099EF;  color: white;border-radius: 50%; text-align: center;line-height: 30px;font-size: 16px;margin-right: 10px;font-weight: bold;">{tweet["user_name"][0]}</span><b>{tweet["user_name"]}</b></h5><div class="p-2"></div><div class="p-2"><i class="fa-regular fa-clock fa-xs"></i> <a href="https://www.twitter.com/{tweet["user_name"]}/status/{tweet["message_id"]}">{tweet["date"].strftime("%d/%m/%y")}</a></div></div><div class="card-body"><p class="card-text">{tweet["translated_text"]}</p></div><div class="card-footer d-flex justify-content-between">{eng_type}<div class="p-2"><i class="fa-solid fa-chart-column fa-xs"></i> {format_number(tweet["engagements"])}</div><div class="p-2"><i class="fa-regular fa-eye fa-xs"></i> {format_number(tweet["views"])}</div><div class="p-2"><i class="fa-solid fa-retweet fa-xs"></i> {format_number(tweet["share"])}</div><div class="p-2"><i class="fas fa-heart  fa-xs"></i> {format_number(tweet["likes"])}</div><div class="p-2"><i class="fas fa-comments fa-xs"></i> {format_number(tweet["comments"])}</div></div></div><br/>'
                    st.write(tweet_card, unsafe_allow_html= True)
    else:
        st.write("NO DATA")