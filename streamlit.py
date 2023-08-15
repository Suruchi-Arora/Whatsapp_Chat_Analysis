import streamlit as st
import preprocess,helper,comparison
import matplotlib.pyplot as plt
import emoji,re

from wordcloud import WordCloud
import numpy as np

init=st.sidebar.selectbox("Select",["Intro","Whatsapp Chat Analysis"])
if init=="Intro":
    st.image("logo_whatsapp.png")
    st.title("Whasapp Chat Analyzer")
    st.write("Introduction to WhatsApp Chat Analysis\nHave you ever wondered what insights you could gain from your WhatsApp conversations? WhatsApp chat analysis is a powerful technique that allows you to uncover trends, sentiments, and key topics within your chats. Whether you're curious about the frequency of certain words, the most used emojis, or the overall tone of your chats, this analysis can provide valuable information.")
    st.subheader("What WhatsApp Chat Analysis Does:")
    st.write("It can help you:\n\n • Discover Word Usage\n\n• Emotion and Sentiment\n\n • Emoji Insights\n\n • Topic Identification\n\n •Visualize Data")
    st.subheader("How to Prepare Your WhatsApp Chat File:")
    st.write("To analyze your WhatsApp chat, you need to prepare a chat file. Here's how you can do it:\n\nOpen WhatsApp on Mobile: Launch the WhatsApp application on your mobile device.\n\nExport the Chat: Navigate to the chat you want to analyze, open the chat options, and look for the 'Export Chat' feature. This feature allows you to export the chat as a text file.\n\nChoose Export Format: Select the export format. For analysis purposes, choose the 'Without Media' option to focus on the text content of the chat.\n\nSave the File: Choose a location to save the exported chat file. Make sure you remember where you saved it for the next steps.\n\nOnce you've exported the chat as a text file, you're ready to analyze it using the tools or scripts designed for WhatsApp chat analysis.")
    
elif init=="Whatsapp Chat Analysis":
    # st.subheader("Please Select Drop your Chat file !")
    uploaded_file = st.sidebar.file_uploader("Choose your chat file")
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()         # To read file as bytes:
        data=bytes_data.decode('utf-8')

        df=preprocess.process_data(data)

        users=df['user'].unique().tolist()
        users.remove('group_notif')
        users.sort()
        users.insert(0,'Overall')

        filtered_df = df[
            ~(df['message'] == "You deleted this message\n") &
            ~(df['message'] == "<Media omitted>\n") &
             ~(df['user'] == "group_notif") &
            ~(df['message'] == "Missed voice call\n")&
            ~(df['message'] == "Missed video call\n")
            ]
        

        opt = st.sidebar.selectbox("Which Analysis",["Chat Analysis","Comparison among Users"])
        if opt=="Chat Analysis":
            name=st.sidebar.selectbox("Individual/Overall Analysis? ",users)
            st.title(f"Analysis of {name} 🕵️‍♀️")            # analysis
            if name=="Overall":
                this=filtered_df
            else:
                this=filtered_df[filtered_df['user']==name]
            st.title("Statistics")
            
            a1,a2,a3,a4=helper.analysis(name,df)
            a,b,c,d=st.columns(4)
            with a:
                st.subheader('Messages')
                st.title(a1)
            with b:
                st.subheader("Media Shared")
                st.title(a2)
            with c:
                st.subheader("URLs Shared")
                st.title(a3)
            with d:
                st.subheader("Emojis Used")
                st.title(a4)

        # Mostly active users
            if name=="Overall":
                st.title("Users Activity")
                vc,busy_df=helper.most_busy_users(filtered_df)
                fig,ax=plt.subplots()

                a,b=st.columns(2)
                with a:
                    ax.bar(vc.index,vc.values)
                    plt.xticks(rotation="vertical")
                    st.pyplot(fig)
                with b:
                    st.dataframe(busy_df)


            # WORDCLOUD
            st.title("Wordcloud")
            text=this['message'].str.cat(sep='')
            contains_letter = bool(re.search(r'[a-zA-Z]', text))

            # Print the result
            if not contains_letter:
                st.markdown("Sorry, no text available for Word Cloud.")
                
            else:
                wc=WordCloud(width=500,height=500,background_color="white")
                s=this['message'].str.cat(sep="")

                df_wc=wc.generate(s)
                fig,ax=plt.subplots()
                ax.imshow(df_wc)
                st.pyplot(fig)

        # MOST_COMMON_WORDS_GRAPH
            st.title("Most Common Words Graph")
            cmn_wrds_df=helper.cmn_wrds(this)
            wrds=cmn_wrds_df[0]
            cnt=cmn_wrds_df[1]
            fig,ax=plt.subplots()
            ax.barh(wrds,cnt)
            plt.xticks(rotation="vertical")
            st.pyplot(fig)
        
            

            #Monthly Timeline
            st.title("Monthly Timeline")
            mt=helper.month_timeline(this)
            # st.dataframe(mt[["year","month","message"]])
            fig,ax=plt.subplots()
            ax.plot(mt['month_year'],mt['message'],color="purple")
            plt.xticks(rotation="vertical")
            st.pyplot(fig)

            # Daily Timeline
            st.title("Daily Timeline")
            dtime=helper.daily_timeline(this)
            # st.dataframe(mt[["year","month","message"]])
            fig,ax=plt.subplots()
            ax.plot(dtime['dt'],dtime['message'],color="green")
            plt.xticks(rotation="vertical")
            st.pyplot(fig)

            # Mostly Emojis Used
            st.title("Emojis Analysis")
            col1,col2=st.columns(2)
            emojis_cnt_df=helper.emoji_cnt(this)
            if emojis_cnt_df.empty:
                st.write("No emojis used in the data.")
            else:
                with col1:
                    st.dataframe(emojis_cnt_df)
                with col2:
                    fig, ax = plt.subplots()
                    ax.pie(emojis_cnt_df['Count'].head(6), labels=emojis_cnt_df['Emoji'].head(6), autopct="%0.2f")
                    st.pyplot(fig)

            

            col1,col2=st.columns(2)
            with col2:
                # Busiest Month
                st.title("Busiest Month")
                mt=helper.busy_month(this)
                # st.dataframe(mt)
                fig,ax=plt.subplots()
                ax.bar(mt['Month'],mt['Total Messages'],color="blue")
                plt.xticks(rotation="vertical")
                st.pyplot(fig)

            with col1:
                #Busiest Day
                st.title("Busiest Day")
                bd=helper.busy_day(this)
                # st.dataframe(mt)
                fig,ax=plt.subplots()
                ax.bar(bd['Day_Name'],bd['Total Messages'],color="red")
                plt.xticks(rotation="vertical")
                st.pyplot(fig)

            

        else:
            comparison.comp(filtered_df)









        
            
                



                



        



