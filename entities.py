import streamlit as st
from opsci_toolbox.helpers.dataviz import generate_wordcloud, fig_bar_trend
import matplotlib.pyplot  as plt 
import pandas as pd

date = st.session_state['date']
txt_query = st.session_state['txt_query']
ignore_case = st.session_state['ignore_case']
ignore_accent = st.session_state['ignore_accent']
match_word = st.session_state['match_word']
df = st.session_state['df']
df_filter = st.session_state['df_filter']

NER_type = st.sidebar.selectbox("Entity Type", ['Organizations', "Persons", "Locations"], index = 0)

NER_type = {'Organizations': 'ORG', 'Persons': 'PERSON', 'Locations': 'LOC'}.get(NER_type)


metrics = {
'posts' : ('message_id',"nunique"),
'views': ('views', 'sum'),
'engagements': ('engagements', 'sum'),
'share': ('share', 'sum'),
'likes': ('likes', 'sum'),
'comments': ('comments', 'sum'),
'channels' : ('channels', 'sum')
}

df_exploded = df_filter.explode(["NER_type", "NER_text"]).dropna(subset=["NER_text"]).reset_index(drop=True)

col1, col2 = st.columns(2, gap="medium")

with col1:
    st.title("Telegram")
    # for ner_type in list(df_exploded['NER_type'].unique()):
    #     st.title(ner_type)
    current_df = df_exploded[(df_exploded['NER_type'] == NER_type) & (df_exploded['plateforme'] =="Telegram")]
    if len(current_df) > 0:
        current_df_gb = current_df.groupby(["message_id", "NER_text"]).agg(**{"channels" : ("user_id", "nunique"), 'views': ('views', 'max'),'engagements': ('engagements', 'max'),'share': ('share', 'max'),'likes': ('likes', 'max'),'comments': ('comments', 'max')}).reset_index()
        current_df_gb = current_df_gb.groupby(["NER_text"]).agg(**metrics).reset_index().sort_values(by="posts", ascending=False)
        wc = generate_wordcloud(current_df_gb.head(200), "NER_text", "posts", width=3000, height=1500, dpi=72, show=False, colormap="viridis", font_path="/font/InriaSans-Bold.ttf")
        fig = plt.figure(figsize=(10,5))
        plt.imshow(wc, interpolation = "bilinear")
        plt.axis('off')
        st.pyplot(fig)
        fig_bar_entities = fig_bar_trend(current_df_gb.head(25), "NER_text", "posts", "engagements", xaxis_title="", yaxis_title= "Verbatims", zaxis_title = "Engagements", col_hover=["channels", "views", "engagements", "share", "likes", "comments"], height=500, showlegend=False, mode="lines", xaxis_tickangle=-45, marker_line_width=2, marker_line_color="#6dff00", marker_color="#a7ff66", title_text="Coverage & Resonance", yaxis_range="auto", zaxis_range="auto")
        st.write(fig_bar_entities)
    else:
        st.write("NO DATA")

with col2:
    st.title("Twitter")
    current_df = df_exploded[(df_exploded['NER_type'] == NER_type) & (df_exploded['plateforme'] =="Twitter")]
    if len(current_df) > 0:
        current_df_gb = current_df.groupby(["message_id", "NER_text"]).agg(**{"channels" : ("user_id", "nunique"), 'views': ('views', 'max'),'engagements': ('engagements', 'max'),'share': ('share', 'max'),'likes': ('likes', 'max'),'comments': ('comments', 'max')}).reset_index()
        current_df_gb = current_df_gb.groupby(["NER_text"]).agg(**metrics).reset_index().sort_values(by="posts", ascending=False)
        wc = generate_wordcloud(current_df_gb.head(200), "NER_text", "posts", width=3000, height=1500, dpi=72, show=False, colormap="viridis", font_path="/home/erwan/scripts/st_pr_v3/font/InriaSans-Bold.ttf")
        fig = plt.figure(figsize=(10,5))
        plt.imshow(wc, interpolation = "bilinear")
        plt.axis('off')
        st.pyplot(fig)
        fig_bar_entities = fig_bar_trend(current_df_gb.head(25), "NER_text", "posts", "engagements", xaxis_title="", yaxis_title= "Verbatims", zaxis_title = "Engagements", col_hover=["channels", "views", "engagements", "share", "likes", "comments"], height=500, showlegend=False, mode="lines", xaxis_tickangle=-45, marker_line_width=2, marker_line_color="#00ecff", marker_color="#66f3ff", title_text="Coverage & Resonance", yaxis_range="auto", zaxis_range="auto")
        st.write(fig_bar_entities)
    else:
        st.write("NO DATA")