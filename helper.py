# SECTION 1: Imports and Configuration
from urlextract import URLExtract
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import pandas as pd
from collections import Counter
import emoji
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import colorsys
import os
from pathlib import Path

extract = URLExtract()

# SECTION 2: Word Cloud Configuration
def create_custom_colormap():
    """Create a custom color function for word cloud visualization"""
    def color_func(word, font_size, position, orientation, random_state=None, **kwargs):
        hue = np.random.uniform(0.55, 0.85)
        saturation = np.random.uniform(0.6, 0.9)
        value = np.random.uniform(0.7, 1.0)
        rgb = colorsys.hsv_to_rgb(hue, saturation, value)
        return f"rgb({int(rgb[0]*255)}, {int(rgb[1]*255)}, {int(rgb[2]*255)})"
    return color_func

def get_font_path():
    """Find appropriate system font for word cloud"""
    possible_fonts = [
        r"C:\Windows\Fonts\segoeui.ttf",
        r"C:\Windows\Fonts\arial.ttf",
        r"C:\Windows\Fonts\calibri.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        "/System/Library/Fonts/Arial Unicode.ttf"
    ]
    return next((font for font in possible_fonts if os.path.exists(font)), None)

# Initialize WordCloud with professional settings
wc = WordCloud(
    width=1600, height=800,
    background_color='#1f2937',
    mode='RGBA',
    color_func=create_custom_colormap(),
    max_words=200,
    min_font_size=10,
    max_font_size=150,
    random_state=42,
    font_path=get_font_path(),
    prefer_horizontal=0.7,
    relative_scaling=0.5,
    regexp=r"[\w']+",
    collocations=True,
    normalize_plurals=True,
    contour_width=1,
    contour_color='#4b5563',
    repeat=False
)

# SECTION 3: Basic Statistics Functions
def fetch_stats(selected_user, df):
    """Extract basic statistics from chat data"""
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
    """Identify most active users in the chat"""
    x = df['user'].value_counts().head()
    new_df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index()
    new_df.columns = ['name', 'percent']
    new_df['percent'] = new_df['percent'].astype(str) + ' %'
    return x, new_df

# SECTION 4: Text Processing Functions
def remove_non_latin_chars(text):
    """Filter out non-Latin characters from text"""
    return ''.join(char for char in text if ord(char) < 128)

def create_word_cloud(selected_user, df):
    """Generate word cloud visualization from chat messages"""
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    with open('stop_hinglish.txt', 'r') as f:
        stop_words = set(f.read().split())

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    
    def remove_stop_words(message):
        message = remove_non_latin_chars(message)
        return " ".join(word for word in message.lower().split() 
                       if word not in stop_words and len(word) > 2)

    temp['message'] = temp['message'].apply(remove_stop_words)
    return wc.generate(temp['message'].str.cat(sep=" "))

def most_common_words(selected_user, df):
    """Analyze most frequently used words in chat"""
    with open('stop_hinglish.txt', 'r') as f:
        stop_words = set(f.read().split())

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    words = []
    for message in temp['message']:
        message = remove_non_latin_chars(message)
        words.extend(word for word in message.lower().split()
                    if word not in stop_words and len(word) > 2)

    return pd.DataFrame(Counter(words).most_common(20), columns=['name', 'msg'])

# SECTION 5: Emoji Analysis
def is_emoji(s):
    """Check if a character is an emoji"""
    return s in emoji.EMOJI_DATA

def emoji_analysis(selected_user, df):
    """Analyze emoji usage in chat messages"""
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Process emojis and their descriptions
    emojis = []
    emoji_data = []
    
    for message in df['message']:
        emojis.extend(c for c in message if is_emoji(c))
    
    emoji_counts = Counter(emojis)
    emoji_descriptions = {
        '😊': 'Smiling face with smiling eyes - expressing happiness',
        '😃': 'Grinning face with big eyes - showing excitement',
        # ... existing emoji descriptions ...
        'default': 'Other emoji type'
    }
    
    for emoji_char, count in emoji_counts.most_common():
        description = emoji_descriptions.get(emoji_char, emoji_descriptions['default'])
        emoji_data.append({
            'emoji': emoji_char,
            'count': count,
            'description': description
        })
    
    return pd.DataFrame(emoji_data)

# SECTION 6: Timeline Analysis Functions
def timeline(selected_user, df):
    """Generate monthly timeline of chat activity"""
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    timeline['time'] = timeline.apply(lambda x: f"{x['month']}-{x['year']}", axis=1)
    return timeline, timeline[['time', 'message']]

def daily_timeline(selected_user, df):
    """Analyze daily message patterns"""
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

# SECTION 7: Activity Pattern Analysis
def daily_activeness(selected_user, df):
    """Analyze message patterns by day of week"""
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
    """Analyze message patterns by month"""
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    return df['month'].value_counts().reset_index()

def activity_heatmap(selected_user, df):
    """Generate activity heatmap visualization"""
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    period_order = [f"{hour:02d}:00-{(hour+1):02d}:00" for hour in range(24)]
    df['formatted_period'] = df['hour'].apply(lambda x: f"{x:02d}:00-{(x+1):02d}:00")
    
    user_heatmap = df.pivot_table(
        index='day_name',
        columns='formatted_period',
        values='message',
        aggfunc='count'
    ).fillna(0)
    
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    user_heatmap = user_heatmap.reindex(index=days, columns=period_order)
    
    figure1 = create_heatmap(user_heatmap, 'Weekly Activity Pattern')
    figure2 = create_detailed_heatmap(user_heatmap, 'Detailed Weekly Activity Pattern')
    
    return user_heatmap, figure1, figure2

# SECTION 8: Response Time Analysis
def calculate_response_times(df):
    """Calculate response times between messages"""
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
    """Analyze response patterns between users"""
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    return df.groupby('user')['response_time'].agg([
        ('avg_response_time', 'mean'),
        ('min_response_time', 'min'),
        ('max_response_time', 'max'),
        ('response_count', 'count')
    ]).round(2)

# SECTION 9: Helper Visualization Functions
def create_daily_activity_plot(daily_timeline):
    """Create daily activity visualization"""
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
    """Create basic heatmap visualization"""
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
    """Create detailed heatmap with annotations"""
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
    """Update heatmap layout with consistent styling"""
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
