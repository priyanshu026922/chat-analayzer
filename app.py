import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt
from matplotlib import font_manager


plt.rcParams['font.family'] = 'Segoe UI Emoji'

st.sidebar.title("CHAT-ANALYZER")

uploaded_file=st.sidebar.file_uploader("Choose a File")

if uploaded_file is not None:
    bytes_data=uploaded_file.getvalue()
    data=bytes_data.decode("utf-8")
    df=preprocessor.preprocess(data)

   

    user_list=df['user'].unique().tolist()
    user_list.remove('Group_Notification')
    user_list.sort()
    user_list.insert(0,"Overall")

    selected_user=st.sidebar.selectbox("CHAT ANALYSIS",user_list)

    if st.sidebar.button("Show Analysis"):
        num_messages,words,num_media_message,num_links=helper.fetch_stats(selected_user,df)
        
        st.title("TOP STATISTICS")
        col1,col2,col3,col4=st.columns(4)



        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Total media shared")
            st.title(num_media_message)
        with col4:
            st.header("Total links shared")
            st.title(num_links)


        #monthy timeline
        st.title("Monthly Timeline")
        timeline=helper.monthly_timeline(selected_user,df)
        fig,ax=plt.subplots()
        ax.plot(timeline['time'],timeline['message'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
 
        #daily timeline
        st.title("Daily Timeline")
        timeline1=helper.daily_timeline(selected_user,df)
        fig,ax=plt.subplots()
        ax.plot(timeline1['date_num'],timeline1['message'],color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #activity map
        st.title('Activity Map')
        col1,col2=st.columns(2)
        with col1:
           st.header("Most Busy Day")
           busy_day=helper.week_activity_map(selected_user,df)
           fig,ax=plt.subplots(figsize=(14,10))
           ax.bar(busy_day.index,busy_day.values)
           plt.xticks(rotation='vertical')
           st.pyplot(fig)
        
        with col2:
           st.header("Most Busy Month")
           busy_month=helper.month_activity_map(selected_user,df)
           fig,ax=plt.subplots(figsize=(14,10))
           ax.bar(busy_month.index,busy_month.values,color='orange')
           plt.xticks(rotation='vertical')
           st.pyplot(fig)


        #busiest users in the group
        if selected_user=='Overall':
            
            x,new_df=helper.busiest_users(df)

            fig,ax=plt.subplots()
            
            col1,col2=st.columns(2)
            with col1:
             st.title("Most Busiest Users")
             ax.bar(x.index,x.values)
             plt.xticks(rotation='vertical')
             st.pyplot(fig)
            with col2:
             st.title("Contribution in group")
             st.dataframe(new_df)
       




       #wordcloud 
        st.title("WordCloud")
        df_wc_image=helper.createWordCloud(selected_user,df)
        fig,ax=plt.subplots()
        ax.imshow(df_wc_image)
        st.pyplot(fig)



       #most common used word
        most_common_df=helper.most_commin_used_word(selected_user,df)
        st.title("Most Common Used")
        fig,ax=plt.subplots()
        ax.bar(most_common_df[0],most_common_df[1])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)


        ##emoji analyzer
        emoji_df=helper.emoji_count(selected_user,df)
        st.title("Most Frequent Emojis")
        col1,col2=st.columns(2)
        with col1:
           st.dataframe(emoji_df)
        with col2:
           fig, ax = plt.subplots()
           ax.pie(emoji_df[1].head(10),
           labels=emoji_df[0].head(10),
           autopct="%0.2f")
           st.pyplot(fig)
        
       