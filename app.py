import streamlit as st
import preprocessor
from wordcloud import WordCloud
import helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)
    
    # fetch unique user list
    user_list = df['user'].unique().tolist()
    
    # Remove 'group_notification' from the user list if it exists
    if 'group_notification' in user_list:
        user_list.remove('group_notification')
    
    user_list.sort()
    user_list.insert(0, 'Overall')
    
    selected_user = st.sidebar.selectbox('Show Analysis wrt', user_list)
    num_msgs, num_words, num_of_media, links_length, links, filtered_df = helper.fetch_stats(selected_user, df)
    
    # Display the DataFrame according to the selected user
    st.dataframe(filtered_df)
    
    ## Stats 
    if st.sidebar.button('Show analysis'):
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.header('Total messages')
            st.title(num_msgs)
        with col2:
            st.header('Total Words in msg')
            st.title(num_words)
        with col3:
            st.header('Total Media omitted')
            st.title(num_of_media)
        with col4:
            st.header('Total Links shared')
            st.title(links_length)
        with col5:
            st.header('Links are given below')
            st.write(links)
        # Bussiest guy in group
        if selected_user == 'Overall':
            st.title('Busiest person in this group')
            x, new_df = helper.busiest_persons(df)
            fig, ax = plt.subplots()
            col1, col2 = st.columns(2)
            with col1:
                ax.bar(x.index, x.values, color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        # Generate and display the word cloud
        st.title("Word Cloud")
        df_wc = helper.create_word_cloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        #ax.axis("off")
        st.pyplot(fig)

        # Generate the most common words df
        most_common_df = helper.most_common_words(selected_user, df)
        # st.dataframe(most_common_df)
        fig, ax = plt.subplots()
        
        # Correct way to access the columns by name
        ax.barh(most_common_df['name'], most_common_df['msg'], color='blue')
        plt.xticks(rotation='vertical')
        
        st.title('Most common words')
        st.pyplot(fig)
        # emojis_analysis
        emoji_df = helper.emoji_analysis(selected_user,df)
        st.title('Most common emojis used by:')
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(emoji_df)
        with col2:
             fig, ax = plt.subplots()
             ax.pie(emoji_df['count'].head(10), labels=emoji_df['emoji'].head(10), autopct='%1.1f%%')
             ax.set_title('Most Common Emojis')
             st.pyplot(fig) 
        # Mountly timeline
        st.title("Mountly timeline")
        col1, col2 = st.columns(2)
        timeline , timeline_df  = helper.timeline(selected_user,df)
        with col1:
            st.dataframe(timeline_df)
        with col2:
            fig , ax = plt.subplots()
            ax.plot(timeline['time'], timeline['message'],color = 'red')
            plt.xticks(rotation = "vertical")
            st.pyplot(fig)
 
        # Daily timeline
        st.title('Daily Timeline')
        daily_timeline = helper.daily_timeline(selected_user,df)
        fig , ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'],color = 'black')
        plt.xticks(rotation = "vertical")
        st.pyplot(fig)
        # daily activeness
        daily_activeness = helper.daily_activeness(selected_user,df)
        st.title('Daily Map')
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(daily_activeness)
        with col2:
            st.header('Busy day')
            fig , ax = plt.subplots()
            ax.barh(daily_activeness['day_name'],daily_activeness['count'] , color = 'green')
            plt.xticks(rotation = "vertical")
            st.pyplot(fig)
        # mountly activeness
        st.title('Mountly Map')
        col1, col2 = st.columns(2)  
        montly_activeness = helper.montly_activeness(selected_user,df)
        with col1:
            st.dataframe(montly_activeness)
        with col2:
            st.header('Busy month')
            fig , ax = plt.subplots()
            ax.barh(montly_activeness['month'],montly_activeness['count'] , color = 'orange')
            plt.xticks(rotation = "vertical")
            st.pyplot(fig)
        # Heat map    
        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user,df)
        fig,ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)    








           
   

        






