import pandas as pd
import numpy as np
import re
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from collections import Counter
from urlextract import URLExtract
from wordcloud import WordCloud, STOPWORDS
import streamlit as st
import emoji

# =============================================
# SECTION 1: INITIALIZATION
# =============================================

extract = URLExtract()

# Initialize stopwords for word cloud
stop_words = set(STOPWORDS)
custom_stopwords = [
    'media', 'omitted', 'https', 'http', 'www', 'com', 'message', 'deleted',
    'ha', 'le', 'ki', 'ke', 'hi', 'me', 'ki', 'bhi', 'ko', 'hai', 'ho',
    'kar', 'ne', 'se', 'to', 'kya', 'tum', 'tha', 'for', 'the', 'have',
    'has', 'had', 'with', 'without', 'this', 'that', 'there', 'these', 'those'
]
stop_words.update(custom_stopwords)

# Configure wordcloud styling
wc = WordCloud(
    width=800,
    height=400,
    background_color='black',
    stopwords=stop_words,
    max_words=200,
    min_font_size=5,
    max_font_size=100,
    collocations=True,
    normalize_plurals=True,
    contour_width=1,
    contour_color='#4b5563',
    repeat=False
)

# =============================================
# SECTION 2: BASIC STATISTICS FUNCTIONS
# =============================================

def fetch_stats(selected_user, df):
    """
    Extract basic statistics from chat data
    
    Parameters:
    -----------
    selected_user : str
        User to filter by or 'Overall' for all users
    df : pandas.DataFrame
        Preprocessed chat dataframe
        
    Returns:
    --------
    tuple
        Statistics including message count, word count, media count, etc.
    """
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    # Calculate message stats
    num_msgs = df.shape[0]
    msgs = []
    for msg in df['message']:
        msgs.extend(msg.split())
    num_words = len(msgs)
    
    # Count media and links
    num_of_media = df[df['message'] == '<Media omitted>\n'].shape[0]
    links = []
    for message in df['message']:
        urls = extract.find_urls(message)
        links.extend(urls)
    links_length = len(links)
    
    return num_msgs, num_words, num_of_media, links_length, links, df


def busiest_persons(df):
    """
    Identify most active users in the chat
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Preprocessed chat dataframe
        
    Returns:
    --------
    tuple
        Raw counts and percentage dataframe
    """
    x = df['user'].value_counts().head()
    new_df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index()
    new_df.columns = ['name', 'percent']
    new_df['percent'] = new_df['percent'].astype(str) + ' %'
    return x, new_df

# =============================================
# SECTION 3: TEXT PROCESSING FUNCTIONS
# =============================================

def remove_non_latin_chars(text):
    """
    Filter out non-Latin characters from text
    
    Parameters:
    -----------
    text : str
        Input text to filter
        
    Returns:
    --------
    str
        Filtered text with only Latin characters
    """
    return ''.join(char for char in text if ord(char) < 128)


def create_word_cloud(selected_user, df):
    """
    Generate word cloud visualization from chat messages
    
    Parameters:
    -----------
    selected_user : str
        User to filter by or 'Overall' for all users
    df : pandas.DataFrame
        Preprocessed chat dataframe
        
    Returns:
    --------
    wordcloud.WordCloud
        Word cloud object ready for visualization
    """
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Filter out media messages and system notifications
    df = df[df['message'] != '<Media omitted>\n']
    df = df[df['user'] != 'group_notification']

    # Combine all messages into one text
    words = []
    for message in df['message']:
        # Skip links
        if ('http://' not in message) and ('https://' not in message):
            # Extract Latin characters only
            cleaned_message = remove_non_latin_chars(message.lower())
            words.extend(cleaned_message.split())
    
    # Filter out stopwords
    words = [word for word in words if word not in stop_words]
    
    # Generate word cloud
    cloud = wc.generate(' '.join(words))
    return cloud


def most_common_words(selected_user, df):
    """
    Analyze most frequently used words in chat
    
    Parameters:
    -----------
    selected_user : str
        User to filter by or 'Overall' for all users
    df : pandas.DataFrame
        Preprocessed chat dataframe
        
    Returns:
    --------
    pandas.DataFrame
        DataFrame with most common words and their frequencies
    """
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Filter out media messages and system notifications
    df = df[df['message'] != '<Media omitted>\n']
    df = df[df['user'] != 'group_notification']

    # Process words
    words = []
    for message in df['message']:
        # Skip links
        if ('http://' not in message) and ('https://' not in message):
            # Extract Latin characters only
            cleaned_message = remove_non_latin_chars(message.lower())
            words.extend(cleaned_message.split())

    # Filter out stopwords
    words_filtered = [word for word in words if word not in stop_words and len(word) > 3]
    
    # Get most common words
    most_common = pd.DataFrame(Counter(words_filtered).most_common(20))
    most_common.columns = ['name', 'msg']
    return most_common

# =============================================
# SECTION 4: EMOJI ANALYSIS
# =============================================

def is_emoji(s):
    """
    Check if a character is an emoji
    
    Parameters:
    -----------
    s : str
        Character to check
        
    Returns:
    --------
    bool
        True if the character is an emoji, False otherwise
    """
    return s in emoji.EMOJI_DATA


def emoji_analysis(selected_user, df):
    """
    Analyze emoji usage in chat messages
    
    Parameters:
    -----------
    selected_user : str
        User to filter by or 'Overall' for all users
    df : pandas.DataFrame
        Preprocessed chat dataframe
        
    Returns:
    --------
    pandas.DataFrame
        DataFrame with emoji counts, sorted by frequency
    """
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
        
    # Filter out system notifications
    df = df[df['user'] != 'group_notification']
    
    # Extract emojis from messages
    emojis = []
    for message in df['message']:
        for char in message:
            if is_emoji(char):
                emojis.append(char)
                
    # Count emojis
    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    
    if emoji_df.empty:
        return pd.DataFrame(columns=['emoji', 'count'])
    else:
        emoji_df.columns = ['emoji', 'count']
        return emoji_df

# =============================================
# SECTION 5: TIMELINE ANALYSIS
# =============================================

def timeline(selected_user, df):
    """
    Generate monthly timeline of chat activity
    
    Parameters:
    -----------
    selected_user : str
        User to filter by or 'Overall' for all users
    df : pandas.DataFrame
        Preprocessed chat dataframe
        
    Returns:
    --------
    tuple
        Timeline dataframe and a simplified version for display
    """
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    timeline['time'] = timeline.apply(lambda x: f"{x['month']}-{x['year']}", axis=1)
    
    return timeline, timeline[['time', 'message']]


def daily_timeline(selected_user, df):
    """
    Analyze daily message patterns
    
    Parameters:
    -----------
    selected_user : str
        User to filter by or 'Overall' for all users
    df : pandas.DataFrame
        Preprocessed chat dataframe
        
    Returns:
    --------
    tuple
        Daily timeline data and visualization figure
    """
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    daily_timeline = df.groupby(['only_date']).agg({
        'message': 'count',
        'user': 'nunique'
    }).reset_index()
    
    daily_timeline['day_name'] = pd.to_datetime(daily_timeline['only_date']).dt.day_name()
    daily_timeline['month'] = pd.to_datetime(daily_timeline['only_date']).dt.month_name()
    daily_timeline['message_ma'] = daily_timeline['message'].rolling(window=7, min_periods=1).mean()
    
    fig = create_daily_activity_plot(daily_timeline)
    return daily_timeline, fig

# =============================================
# SECTION 6: ACTIVITY PATTERN ANALYSIS
# =============================================

def daily_activeness(selected_user, df):
    """
    Analyze message patterns by day of week
    
    Parameters:
    -----------
    selected_user : str
        User to filter by or 'Overall' for all users
    df : pandas.DataFrame
        Preprocessed chat dataframe
        
    Returns:
    --------
    pandas.DataFrame
        DataFrame with activity by day of week
    """
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    daily_counts = df['day_name'].value_counts().reset_index()
    daily_counts.columns = ['day_name', 'count']
    
    all_days = pd.DataFrame({'day_name': day_order})
    daily_activeness = all_days.merge(daily_counts, on='day_name', how='left').fillna(0)
    daily_activeness['count'] = daily_activeness['count'].astype(int)
    
    daily_activeness['day_order'] = pd.Categorical(daily_activeness['day_name'], 
                                                 categories=day_order, ordered=True)
    return daily_activeness.sort_values('day_order').drop('day_order', axis=1)


def montly_activeness(selected_user, df):
    """
    Analyze message patterns by month
    
    Parameters:
    -----------
    selected_user : str
        User to filter by or 'Overall' for all users
    df : pandas.DataFrame
        Preprocessed chat dataframe
        
    Returns:
    --------
    pandas.DataFrame
        DataFrame with activity by month
    """
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    return df['month'].value_counts().reset_index()


def activity_heatmap(selected_user, df):
    """
    Generate activity heatmap visualization
    
    Parameters:
    -----------
    selected_user : str
        User to filter by or 'Overall' for all users
    df : pandas.DataFrame
        Preprocessed chat dataframe
        
    Returns:
    --------
    tuple
        Heatmap data and two visualization figures
    """
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    # Check if there's any data after filtering
    if len(df) == 0:
        st.warning(f"No messages found for user '{selected_user}'")
        return pd.DataFrame(), None, None
    
    # Handle NaN values by dropping them
    df = df.dropna(subset=['hour'])
    
    # Check if there's still data after dropping NaNs
    if len(df) == 0:
        st.warning(f"No valid time data found for user '{selected_user}'")
        return pd.DataFrame(), None, None
    
    # Now safely convert 'hour' to int after removing NaN values
    df['hour'] = df['hour'].astype(int)
    
    # Format hours
    period_order = [f"{hour:02d}:00-{(hour+1):02d}:00" for hour in range(24)]
    df['formatted_period'] = df['hour'].apply(lambda x: f"{x:02d}:00-{(x+1):02d}:00")
    
    # Create pivot table
    user_heatmap = df.pivot_table(
        index='day_name',
        columns='formatted_period',
        values='message',
        aggfunc='count'
    ).fillna(0)
    
    # Define day order for consistent display
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    # Check if we have data in the pivot table
    if not user_heatmap.empty:
        # Get available days and columns
        available_days = [day for day in days if day in user_heatmap.index]
        available_periods = [period for period in period_order if period in user_heatmap.columns]
        
        # Only reindex if we have both days and periods
        if available_days and available_periods:
            user_heatmap = user_heatmap.reindex(
                index=available_days,
                columns=available_periods
            ).fillna(0)
    
    # Create visualizations
    figure1 = create_heatmap(user_heatmap, 'Weekly Activity Pattern')
    figure2 = create_detailed_heatmap(user_heatmap, 'Detailed Weekly Activity Pattern')
    
    return user_heatmap, figure1, figure2

# =============================================
# SECTION 7: RESPONSE TIME ANALYSIS
# =============================================

def calculate_response_times(df):
    """
    Calculate response times between messages
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Preprocessed chat dataframe
        
    Returns:
    --------
    pandas.DataFrame
        DataFrame with response time calculations
    """
    df = df.copy()[df['user'] != 'group_notification']
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')
    
    df['prev_msg_time'] = df['date'].shift()
    df['prev_msg_user'] = df['user'].shift()
    
    different_user_mask = df['user'] != df['prev_msg_user']
    df.loc[different_user_mask, 'response_time'] = (
        df.loc[different_user_mask, 'date'] - 
        df.loc[different_user_mask, 'prev_msg_time']
    ).dt.total_seconds() / 60
    
    return df[df['response_time'] <= 24 * 60]

def analyze_response_patterns(df, selected_user='Overall'):
    """
    Analyze response patterns between users
    
    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame with response time calculations
    selected_user : str, optional
        User to filter by or 'Overall' for all users
        
    Returns:
    --------
    pandas.DataFrame
        DataFrame with aggregated response metrics by user
    """
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    return df.groupby('user')['response_time'].agg([
        ('avg_response_time', 'mean'),
        ('min_response_time', 'min'),
        ('max_response_time', 'max'),
        ('response_count', 'count')
    ]).round(2)

# =============================================
# SECTION 8: VISUALIZATION FUNCTIONS
# =============================================

def create_daily_activity_plot(daily_timeline):
    """
    Create daily activity visualization
    
    Parameters:
    -----------
    daily_timeline : pandas.DataFrame
        DataFrame containing daily message counts and dates
        
    Returns:
    --------
    plotly.graph_objects.Figure
        Interactive plot of daily message activity
    """
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=daily_timeline['only_date'],
        y=daily_timeline['message'],
        mode='markers',
        name='Daily Messages',
        marker=dict(
            size=8,
            color=daily_timeline['message'],
            colorscale=[
                [0, 'rgb(49, 54, 149)'],
                [0.5, 'rgb(116, 173, 209)'],
                [1, 'rgb(215, 48, 39)']
            ],
            showscale=True,
            colorbar=dict(title='Message Count')
        )
    ))
    
    fig.add_trace(go.Scatter(
        x=daily_timeline['only_date'],
        y=daily_timeline['message_ma'],
        mode='lines',
        name='7-day Moving Average',
        line=dict(color='rgb(253, 174, 97)', width=2)
    ))
    
    fig.update_layout(
        title='Daily Message Activity',
        xaxis_title='Date',
        yaxis_title='Number of Messages',
        template='plotly_white',
        hovermode='x unified',
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        )
    )
    
    return fig

def create_heatmap(data, title):
    """
    Create basic heatmap visualization
    
    Parameters:
    -----------
    data : pandas.DataFrame
        DataFrame containing heatmap data
    title : str
        Title for the heatmap
        
    Returns:
    --------
    plotly.graph_objects.Figure
        Basic heatmap visualization
    """
    figure = go.Figure(data=[go.Heatmap(
        z=data.values,
        x=data.columns,
        y=data.index,
        colorscale='Viridis',
        showscale=True,
        hoverongaps=False,
        hovertemplate='Day: %{y}<br>Time: %{x}<br>Messages: %{z}<extra></extra>'
    )])
    
    return update_heatmap_layout(figure, title)

def create_detailed_heatmap(data, title):
    """
    Create detailed heatmap with annotations
    
    Parameters:
    -----------
    data : pandas.DataFrame
        DataFrame containing heatmap data
    title : str
        Title for the heatmap
        
    Returns:
    --------
    plotly.graph_objects.Figure
        Detailed heatmap with cell annotations
    """
    figure = go.Figure(data=[go.Heatmap(
        z=data.values,
        x=data.columns,
        y=data.index,
        colorscale='Viridis',
        text=data.values.astype(int),
        texttemplate="%{text}",
        textfont={"size": 12, "color": "white", "family": "Arial"},
        showscale=True,
        hoverongaps=False,
        hovertemplate='Day: %{y}<br>Time: %{x}<br>Messages: %{z}<extra></extra>'
    )])
    
    return update_heatmap_layout(figure, title)

def update_heatmap_layout(figure, title):
    """
    Update heatmap layout with consistent styling
    
    Parameters:
    -----------
    figure : plotly.graph_objects.Figure
        Figure object to update
    title : str
        Title for the heatmap
        
    Returns:
    --------
    plotly.graph_objects.Figure
        Updated figure with consistent styling
    """
    figure.update_layout(
        title=dict(
            text=title,
            x=0.5,
            y=0.95,
            xanchor='center',
            yanchor='top',
            font=dict(size=24, color='white', family='Arial Black')
        ),
        xaxis=dict(
            side='bottom',
            tickangle=45,
            title='Time of Day',
            title_font=dict(size=16, color='white'),
            tickfont=dict(size=12, color='white'),
            gridcolor='rgba(255, 255, 255, 0.1)',
            linecolor='white'
        ),
        yaxis=dict(
            side='left',
            title='Day of Week',
            title_font=dict(size=16, color='white'),
            tickfont=dict(size=14, color='white'),
            gridcolor='rgba(255, 255, 255, 0.1)',
            linecolor='white'
        ),
        font=dict(family='Arial'),
        plot_bgcolor='#1f2937',
        paper_bgcolor='#1f2937',
        margin=dict(l=80, r=80, t=100, b=80),
        width=1400,
        height=700
    )
    return figure

def generate_chat_summary(df):
    """
    Generate a concise summary of the WhatsApp chat.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Preprocessed chat dataframe
    
    Returns:
    --------
    str
        Concise summary string
    """
    total_msgs = df.shape[0]
    total_users = df['user'].nunique()
    most_active = df['user'].value_counts().idxmax()
    summary = (
        f"This WhatsApp chat has {total_msgs} messages, "
        f"{total_users} participants, and the most active user is '{most_active}'."
    )
    return summary
