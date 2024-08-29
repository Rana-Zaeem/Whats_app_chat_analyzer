from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji

extract = URLExtract()
wc = WordCloud(width=500, height=500, min_font_size=15, background_color='white')

def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    num_msgs = df.shape[0]
    
    msgs = []
    for msg in df['message']:
        msgs.extend(msg.split())
    num_words = len(msgs)
    
    num_of_media = df[df['message'] == '<Media omitted>\n'].shape[0]
    
    links = []
    for message in df['message']:
        urls = extract.find_urls(message)
        links.extend(urls)
    links_length = len(links)
    
    return num_msgs, num_words, num_of_media, links_length, links,df

def busiest_persons(df):
    x = df['user'].value_counts().head()
    new_df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index()
    new_df.columns = ['name', 'percent']
    new_df['percent'] = new_df['percent'].astype(str) + ' %'
    return x, new_df

def create_word_cloud(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    with open('stop_hinglish.txt', 'r') as f:
        stop_words = set(f.read().split())

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    
    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    temp['message'] = temp['message'].apply(remove_stop_words)
    
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc

def most_common_words(selected_user, df):
    with open('stop_hinglish.txt', 'r') as f:
        stop_words = set(f.read().split())

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    words = []

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20), columns=['name', 'msg'])
    return most_common_df

def is_emoji(s):
    return s in emoji.EMOJI_DATA

def emoji_analysis(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if is_emoji(c)])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))), columns=['emoji', 'count'])
    return emoji_df
def timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    timeline=df.groupby(['year', 'month_num','month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
       time.append(timeline['month'][i] + '-' + str(timeline['year'][i]))
    timeline['time'] = time   
    timeline_df = timeline[['time', 'message']]
    return timeline  , timeline_df
def daily_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    daily_timeline = df.groupby(['only_date']).count()['message'].reset_index()
    return daily_timeline  
def daily_activeness(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    daily_activeness = df['day_name'].value_counts().reset_index()
    return daily_activeness
def montly_activeness(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    montly_activeness = df['month'].value_counts().reset_index()
    return montly_activeness  
def activity_heatmap(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return user_heatmap



