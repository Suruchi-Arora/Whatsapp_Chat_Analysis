import pandas as pd
import re
import datetime as dt

def process_data(data):
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{1,2}\u202f[APap][Mm]\s-\s'
    messages=re.split(pattern,data)[1:]
    dates=re.findall(pattern,data)

    df=pd.DataFrame({'user_message':messages,"message_date":dates})
    df['message_date'] = pd.to_datetime(df['message_date'], format='%m/%d/%y, %H:%M\u202f%p - ')

    #Seperate users and their respective messages
    users=[]
    messages=[]

    for msg in df['user_message']:
        line=re.split('([\w\W]+?):\s',msg)
        if(line[1:]):
            users.append(line[1])
            messages.append(line[2])
        else:
            users.append('group_notif')
            messages.append(line[0])
            
            
    df['user']=users
    df['message']=messages

    df.drop(columns={'user_message'},inplace=True)

    df['year']=df['message_date'].dt.year
    df['month']=df['message_date'].dt.month_name()
    df['day']=df['message_date'].dt.day
    df['hour']=df['message_date'].dt.hour
    df['minute']=df['message_date'].dt.minute


    return df







    
