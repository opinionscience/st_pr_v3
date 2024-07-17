import streamlit as st
import pandas as pd
from  lib.helpers import format_number
from opsci_toolbox.apis.webscraping import url_get_domain, url_add_protocol


df =  st.session_state['df']
df_filter =  st.session_state['df_filter']

sort_by = st.sidebar.selectbox("Sort by", ["posts", "engagements", "views", "channels"], index=0)
nb_urls = st.sidebar.number_input("Number of Top URLS", value = 10)


df_urls = df_filter[(df_filter['url'].notna()) & (df_filter['url'].str.len()>0)]
metrics = {
'posts' : ('message_id',"nunique"),
'views': ('views', 'sum'),
'engagements': ('engagements', 'sum'),
'share': ('share', 'sum'),
'likes': ('likes', 'sum'),
'comments': ('comments', 'sum'),
'channels': ('user_id', 'nunique')
}

df_urls_gb = df_urls.groupby(['plateforme','url']).agg(**metrics).reset_index().sort_values(by='posts', ascending=False)
df_domains_gb = df_urls.groupby(["plateforme", "domain"]).agg(**metrics).reset_index().sort_values(by='posts', ascending=False)


col1, col2 = st.columns(2, gap="medium")

with col1:
    st.title("Telegram")
    st.subheader("Top URLs")
    if len(df_urls_gb[df_urls_gb['plateforme']=="Telegram"]) >0:
        for i, row in df_urls_gb[df_urls_gb['plateforme']=="Telegram"].sort_values(by=sort_by, ascending=False).head(nb_urls).iterrows():
            card=f'<div class="card"><div class="card-header d-flex justify-content-between"><div class="col"><p class="p-2"><span style=" display: inline-block;width: 30px;height: 30px;background-color: #0099EF; color: white;border-radius: 50%; text-align: center;line-height: 30px;font-size: 16px;margin-right: 10px;font-weight: bold;">{url_get_domain(row["url"])[0]}</span><b><a href="{row["url"]}" target="_blank">{row["url"]}</a></b></p></div><div class="col d-flex justify-content-between"><div class="p-2"><i class="fa-solid fa-user fa-xs"></i> {format_number(row["channels"])}</div><div class="p-2"><i class="fa-solid fa-message fa-xs"></i> {format_number(row["posts"])}</div><div class="p-2"><i class="fa-solid fa-chart-column fa-xs"></i> {format_number(row["engagements"])}</div><div class="p-2"><i class="fa-regular fa-eye fa-xs"></i> {format_number(row["views"])}</div></div></div></div><br/>'
            st.markdown(card, unsafe_allow_html= True)
    else:
        st.write("NO DATA")
    st.subheader("Top domains")
    if len(df_domains_gb[df_domains_gb['plateforme']=="Telegram"]) >0:
        for i, row in df_domains_gb[df_domains_gb['plateforme']=="Telegram"].sort_values(by=sort_by, ascending=False).head(nb_urls).iterrows():
            card=f'<div class="card"><div class="card-header d-flex justify-content-between"><div class="col"><p class="p-2"><span style=" display: inline-block;width: 30px;height: 30px;background-color: #0099EF; color: white;border-radius: 50%; text-align: center;line-height: 30px;font-size: 16px;margin-right: 10px;font-weight: bold;">{row["domain"][0]}</span><b><a href="{url_add_protocol(row["domain"])}" target="_blank">{row["domain"]}</a></b></p></div><div class="col d-flex justify-content-between"><div class="p-2"><i class="fa-solid fa-user fa-xs"></i> {format_number(row["channels"])}</div><div class="p-2"><i class="fa-solid fa-message fa-xs"></i> {format_number(row["posts"])}</div><div class="p-2"><i class="fa-solid fa-chart-column fa-xs"></i> {format_number(row["engagements"])}</div><div class="p-2"><i class="fa-regular fa-eye fa-xs"></i> {format_number(row["views"])}</div></div></div></div><br/>'
            st.markdown(card, unsafe_allow_html= True)
    else:
        st.write("NO DATA")


with col2:
    st.title("Twitter")
    st.subheader("Top URLs")
    if len(df_urls_gb[df_urls_gb['plateforme']=="Twitter"]) >0:
        for i, row in df_urls_gb[df_urls_gb['plateforme']=="Twitter"].sort_values(by=sort_by, ascending=False).head(nb_urls).iterrows():
            card=f'<div class="card"><div class="card-header d-flex justify-content-between"><div class="col"><p class="p-2"><span style=" display: inline-block;width: 30px;height: 30px;background-color: #0099EF; color: white;border-radius: 50%; text-align: center;line-height: 30px;font-size: 16px;margin-right: 10px;font-weight: bold;">{url_get_domain(row["url"])[0]}</span><b><a href="{row["url"]}" target="_blank">{row["url"]}</a></b></p></div><div class="col d-flex justify-content-between"><div class="p-2"><i class="fa-solid fa-user fa-xs"></i> {format_number(row["channels"])}</div><div class="p-2"><i class="fa-solid fa-message fa-xs"></i> {format_number(row["posts"])}</div><div class="p-2"><i class="fa-solid fa-chart-column fa-xs"></i> {format_number(row["engagements"])}</div><div class="p-2"><i class="fa-regular fa-eye fa-xs"></i> {format_number(row["views"])}</div></div></div></div><br/>'
            st.markdown(card, unsafe_allow_html= True)
    else:
        st.write("NO DATA")

    st.subheader("Top Domains")
    if len(df_domains_gb[df_domains_gb['plateforme']=="Twitter"]) >0:
        for i, row in df_domains_gb[df_domains_gb['plateforme']=="Twitter"].sort_values(by=sort_by, ascending=False).head(nb_urls).iterrows():
            card=f'<div class="card"><div class="card-header d-flex justify-content-between"><div class="col"><p class="p-2"><span style=" display: inline-block;width: 30px;height: 30px;background-color: #0099EF; color: white;border-radius: 50%; text-align: center;line-height: 30px;font-size: 16px;margin-right: 10px;font-weight: bold;">{row["domain"][0]}</span><b><a href="{url_add_protocol(row["domain"])}" target="_blank">{row["domain"]}</a></b></p></div><div class="col d-flex justify-content-between"><div class="p-2"><i class="fa-solid fa-user fa-xs"></i> {format_number(row["channels"])}</div><div class="p-2"><i class="fa-solid fa-message fa-xs"></i> {format_number(row["posts"])}</div><div class="p-2"><i class="fa-solid fa-chart-column fa-xs"></i> {format_number(row["engagements"])}</div><div class="p-2"><i class="fa-regular fa-eye fa-xs"></i> {format_number(row["views"])}</div></div></div></div><br/>'
            st.markdown(card, unsafe_allow_html= True)
    else:
        st.write("NO DATA")