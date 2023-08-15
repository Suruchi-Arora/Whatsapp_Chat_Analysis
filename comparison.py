import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

def comp(filtered_df):
    def user_avg_lengths(filtered_df):
        user_avg_lengths = []
        for user in filtered_df['user'].unique():
            user_messages = filtered_df[filtered_df['user'] == user]['message']
            msg_lengths = [len(msg.split()) for msg in user_messages]
            user_avg_length = int(np.mean(msg_lengths))
            user_avg_lengths.append((user, user_avg_length))

        avg_df = pd.DataFrame(user_avg_lengths, columns=['User', 'Average Message Length'])
        st.dataframe(avg_df)

    grp_df=filtered_df.groupby(['user','year','month']).count()['message'].reset_index()
    def show_user_message_counts(grp_df):
        time_list = []
        for i in range(grp_df.shape[0]):
            time_list.append(str(grp_df['month'][i]) + "-" + str(grp_df['year'][i]))
        grp_df['month_year'] = time_list
        fig = px.bar(grp_df, x='month_year', y='message', color='user',
                    labels={'message': 'Message Count'},
                    title='User Message Counts by Month and Year')
        fig.update_layout(xaxis_categoryorder='total ascending')
        fig.update_layout(xaxis_tickangle=-90)
        st.plotly_chart(fig)

    def show_daily_message_counts(filtered_df):
        dt_grp = filtered_df.copy()
        dt_grp['dt'] = filtered_df['message_date'].dt.date
        daily_message_count = dt_grp.groupby(['user', 'dt']).size().reset_index(name='message_count')
        custom_colors = ['green', 'orange', 'purple', 'cyan', 'magenta']
        fig = px.line(daily_message_count, x='dt', y='message_count', color='user',
                    color_discrete_sequence=custom_colors,
                    labels={'message_count': 'Message Count'},
                    title='Daily Message Counts by User')
        fig.update_layout(xaxis_title='Date')
        st.plotly_chart(fig)


    def show_message_counts_by_day(filtered_df):
        filtered_df['day_name'] = filtered_df['message_date'].dt.day_name()
        bd = filtered_df.groupby(['user', 'day_name']).size().reset_index(name='total_messages')
        custom_colors = ['green', 'orange', 'purple', 'cyan', 'magenta']

        fig = px.bar(bd, x='day_name', y='total_messages', color='user',
                    color_discrete_sequence=custom_colors,
                    labels={'total_messages': 'Total Messages'},
                    title='Message Counts by Day of the Week for All Users')

        st.plotly_chart(fig)











    
    user_avg_lengths(filtered_df)
    show_user_message_counts(grp_df)
    show_daily_message_counts(filtered_df)
    show_message_counts_by_day(filtered_df)
    
