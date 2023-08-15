import streamlit as st
from urlextract import URLExtract
extractor = URLExtract()

import emoji
from collections import Counter
import pandas as pd
import re

def analysis(name,df):

    
    links_list=[]
    emo=[]
    if name=="Overall":
        messages=df['message'].shape[0]
        media=df[df['message']=="<Media omitted>\n"].shape[0]
        for msg in df['message']:
            links_list.extend(extractor.find_urls(msg))
        links=len(links_list)
        for msg in df['message']:
            emo.extend([c for c in msg if c in emoji.UNICODE_EMOJI['en']])
        emos=len(emo)

        
    else:
        temp_df=df[df['user']==name]
        messages=temp_df.shape[0]
        media=temp_df[temp_df['message']=="<Media omitted>\n"].shape[0]
        for msg in temp_df['message']:
            links_list.extend(extractor.find_urls(msg))
        links=len(links_list)
        for msg in temp_df['message']:
            emo.extend([c for c in msg if c in emoji.UNICODE_EMOJI['en']])
        emos=len(emo)
            
    return messages,media,links,emos

def most_busy_users(filtered_df):
    busy_df=(round((filtered_df['user'].value_counts()/filtered_df.shape[0])*100,2).reset_index().rename(columns={'index':'name','user':'percent'}))
    vc=filtered_df['user'].value_counts()

    return vc,busy_df

    
def cmn_wrds(filtered_df):
    chats=[]
    for msg in filtered_df['message']:
        for wrd in msg.split():
            chats.append(wrd)
    return pd.DataFrame(Counter(chats).most_common(15))


def emoji_cnt(filtered_df):
    ems=[] 
    for msg in filtered_df['message']:
        ems.extend([c for c in msg if c in emoji.UNICODE_EMOJI['en']])

    emojis_cnt_df=pd.DataFrame(Counter(ems).most_common(10))
    emojis_cnt_df = emojis_cnt_df.rename(columns={0: "Emoji", 1: "Count"})

    return emojis_cnt_df


def month_timeline(filtered_df):
    time_list=[]
    filtered_df['month_num']=filtered_df['message_date'].dt.month
    timeline=filtered_df.groupby(['year','month_num','month']).count()['message'].reset_index()
    for i in range(timeline.shape[0]):
        time_list.append(str(timeline['month'][i])+"-"+str(timeline['year'][i]))
    timeline['month_year']=time_list

    return timeline

def daily_timeline(filtered_df):
    filtered_df['dt']=filtered_df['message_date'].dt.date
    dailty_timeline=filtered_df.groupby('dt').count()['message'].reset_index()
    return dailty_timeline


def busy_month(filtered_df):
    mnth_cnt=filtered_df['month'].value_counts().reset_index()
    mnth_cnt=mnth_cnt.rename(columns={"index":"Month","month":"Total Messages"})
    return mnth_cnt

def busy_day(filtered_df):
    filtered_df['day_name']=filtered_df['message_date'].dt.day_name()
    bd=filtered_df['day_name'].value_counts().reset_index()
    bd=bd.rename(columns={"index":"Day_Name","day_name":"Total Messages"})
    return bd







   


