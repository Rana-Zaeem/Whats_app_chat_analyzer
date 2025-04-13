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

# Enhanced WordCloud configuration with professional settings
def create_custom_colormap():
    def color_func(word, font_size, position, orientation, random_state=None, **kwargs):
        # Create a gradient effect based on word frequency
        hue = np.random.uniform(0.55, 0.85)  # Blue-ish range
        saturation = np.random.uniform(0.6, 0.9)
        value = np.random.uniform(0.7, 1.0)
        rgb = colorsys.hsv_to_rgb(hue, saturation, value)
        return f"rgb({int(rgb[0]*255)}, {int(rgb[1]*255)}, {int(rgb[2]*255)})"
    
    return color_func

# Try to find system fonts that support multiple languages
def get_font_path():
    possible_fonts = [
        # Windows fonts
        r"C:\Windows\Fonts\segoeui.ttf",  # Segoe UI
        r"C:\Windows\Fonts\arial.ttf",     # Arial
        r"C:\Windows\Fonts\calibri.ttf",   # Calibri
        # Linux fonts
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        # macOS fonts
        "/System/Library/Fonts/Arial Unicode.ttf"
    ]
    
    for font_path in possible_fonts:
        if os.path.exists(font_path):
            return font_path
    return None

wc = WordCloud(
    width=1600,
    height=800,
    background_color='#1f2937',
    mode='RGBA',
    color_func=create_custom_colormap(),
    max_words=200,
    min_font_size=10,
    max_font_size=150,
    random_state=42,
    font_path=get_font_path(),  # Use system font that supports multiple languages
    prefer_horizontal=0.7,
    relative_scaling=0.5,
    regexp=r"[\w']+",  # Modified regex to better handle special characters
    collocations=True,
    normalize_plurals=True,
    contour_width=1,
    contour_color='#4b5563',
    repeat=False
)

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

def remove_non_latin_chars(text):
    # Filter out non-Latin characters and keep only ASCII characters, numbers, and basic punctuation
    return ''.join(char for char in text if ord(char) < 128)

def create_word_cloud(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    with open('stop_hinglish.txt', 'r') as f:
        stop_words = set(f.read().split())

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    
    def remove_stop_words(message):
        # First remove non-Latin characters
        message = remove_non_latin_chars(message)
        y = []
        for word in message.lower().split():
            if word not in stop_words and len(word) > 2:  # Also filter out very short words
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
        # Remove non-Latin characters
        message = remove_non_latin_chars(message)
        for word in message.lower().split():
            if word not in stop_words and len(word) > 2:  # Filter out very short words
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20), columns=['name', 'msg'])
    return most_common_df

def is_emoji(s):
    return s in emoji.EMOJI_DATA

def emoji_analysis(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Emoji descriptions dictionary
    emoji_descriptions = {
        # Happy emotions
        '😊': 'Smiling face with smiling eyes - expressing happiness',
        '😃': 'Grinning face with big eyes - showing excitement',
        '😄': 'Grinning face with smiling eyes - expressing joy',
        '😁': 'Beaming face with smiling eyes - showing glee',
        '😆': 'Grinning squinting face - expressing laughter',
        '😅': 'Grinning face with sweat - awkward happiness',
        '😂': 'Face with tears of joy - intense laughter',
        '🤣': 'Rolling on the floor laughing - hilarious reaction',
        
        # Love emotions
        '❤️': 'Red heart - expressing love and affection',
        '🥰': 'Smiling face with hearts - feeling loved',
        '😍': 'Heart eyes - showing adoration',
        '😘': 'Face blowing a kiss - sending affection',
        '💕': 'Two hearts - expressing love and harmony',
        
        # Sad emotions
        '😢': 'Crying face - expressing sadness',
        '😭': 'Loudly crying face - intense sadness',
        '😞': 'Disappointed face - showing disappointment',
        '😔': 'Pensive face - expressing thoughtful sadness',
        '😪': 'Sleepy face - showing tiredness',
        
        # Celebration
        '🎉': 'Party popper - celebration and congratulations',
        '🎊': 'Confetti ball - festive celebration',
        '🎈': 'Balloon - party and celebration',
        '✨': 'Sparkles - indicating special or magical moments',
        '🌟': 'Glowing star - excellence or special achievement',
        
        # Nature
        '🌺': 'Hibiscus flower - beauty and nature',
        '🌸': 'Cherry blossom - beauty and spring season',
        '🌼': 'Blossom - representing nature and growth',
        '🌻': 'Sunflower - happiness and nature',
        
        # Objects
        '📱': 'Mobile phone - technology and communication',
        '💻': 'Laptop - work and technology',
        '📷': 'Camera - photography and memories',
        '📚': 'Books - education and learning',
        
        # Default description for unlisted emojis
        'default': 'Other emoji type'
    }

    emojis = []
    emoji_data = []
    
    for message in df['message']:
        message_emojis = [c for c in message if is_emoji(c)]
        emojis.extend(message_emojis)
    
    # Count emojis and create dataset with descriptions
    emoji_counts = Counter(emojis)
    for emoji, count in emoji_counts.most_common():
        description = emoji_descriptions.get(emoji, emoji_descriptions['default'])
        emoji_data.append({
            'emoji': emoji,
            'count': count,
            'description': description
        })
    
    # Create DataFrame with emoji, count, and description
    emoji_df = pd.DataFrame(emoji_data)
    
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
    
    # Group by date and get message count
    daily_timeline = df.groupby(['only_date']).agg({
        'message': 'count',
        'user': 'nunique'  # Count unique users per day
    }).reset_index()
    
    # Add day name and month name for better context
    daily_timeline['day_name'] = pd.to_datetime(daily_timeline['only_date']).dt.day_name()
    daily_timeline['month'] = pd.to_datetime(daily_timeline['only_date']).dt.month_name()
    
    # Calculate 7-day moving average
    daily_timeline['message_ma'] = daily_timeline['message'].rolling(window=7, min_periods=1).mean()
    
    # Create heatmap with custom color scheme
    fig = go.Figure()
    
    # Add the daily message count with custom styling
    fig.add_trace(go.Scatter(
        x=daily_timeline['only_date'],
        y=daily_timeline['message'],
        mode='markers',
        name='Daily Messages',
        marker=dict(
            size=8,
            color=daily_timeline['message'],
            colorscale=[
                [0, 'rgb(49, 54, 149)'],     # Deep blue for low values
                [0.5, 'rgb(116, 173, 209)'],  # Light blue for medium values
                [1, 'rgb(215, 48, 39)']       # Deep red for high values
            ],
            showscale=True,
            colorbar=dict(title='Message Count')
        )
    ))
    
    # Add the moving average line
    fig.add_trace(go.Scatter(
        x=daily_timeline['only_date'],
        y=daily_timeline['message_ma'],
        mode='lines',
        name='7-day Moving Average',
        line=dict(color='rgb(253, 174, 97)', width=2)
    ))
    
    # Update layout for better visualization
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
    
    return daily_timeline, fig

def daily_activeness(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    # Define the correct order of days
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    # Get the value counts and reset index
    daily_counts = df['day_name'].value_counts().reset_index()
    daily_counts.columns = ['day_name', 'count']
    
    # Create a DataFrame with all days to ensure no days are missing
    all_days = pd.DataFrame({'day_name': day_order})
    
    # Merge with actual counts, filling missing values with 0
    daily_activeness = all_days.merge(daily_counts, on='day_name', how='left').fillna(0)
    
    # Convert count to integer
    daily_activeness['count'] = daily_activeness['count'].astype(int)
    
    # Sort according to the day order
    daily_activeness['day_order'] = pd.Categorical(daily_activeness['day_name'], categories=day_order, ordered=True)
    daily_activeness = daily_activeness.sort_values('day_order').drop('day_order', axis=1)
    
    return daily_activeness

def montly_activeness(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    montly_activeness = df['month'].value_counts().reset_index()
    return montly_activeness

def activity_heatmap(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    # Create period labels in 24-hour format with better formatting
    period_order = [f"{hour:02d}:00-{(hour+1):02d}:00" for hour in range(24)]
    df['formatted_period'] = df['hour'].apply(lambda x: f"{x:02d}:00-{(x+1):02d}:00")
    
    # Create a pivot table with proper formatting for days
    user_heatmap = df.pivot_table(
        index='day_name',
        columns='formatted_period',
        values='message',
        aggfunc='count'
    ).fillna(0)
    
    # Reorder the days to start from Monday
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    user_heatmap = user_heatmap.reindex(index=days)
    
    # Make sure all hours are present and format properly
    user_heatmap = user_heatmap.reindex(columns=period_order)
    user_heatmap = user_heatmap.fillna(0)

    # Create first heatmap figure - Clean visualization
    figure1 = go.Figure(data=go.Heatmap(
        z=user_heatmap.values,
        x=user_heatmap.columns,
        y=user_heatmap.index,
        colorscale='Viridis',
        showscale=True,
        colorbar=dict(
            title='Message Count',
            titleside='right',
            thickness=15,
            len=0.75,
            tickfont=dict(size=12),
            titlefont=dict(size=14)
        ),
        hovertemplate='Day: %{y}<br>Time: %{x}<br>Messages: %{z}<extra></extra>'
    ))
    
    # Update layout for the first figure with broader display
    figure1.update_layout(
        title=dict(
            text='Weekly Activity Pattern',
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
        width=1400,  # Increased width
        height=700   # Increased height
    )
    
    # Create second heatmap figure with annotations
    figure2 = go.Figure(data=go.Heatmap(
        z=user_heatmap.values,
        x=user_heatmap.columns,
        y=user_heatmap.index,
        colorscale='Viridis',
        text=user_heatmap.values.astype(int),
        texttemplate="%{text}",
        textfont={"size": 12, "color": "white", "family": "Arial"},
        showscale=True,
        colorbar=dict(
            title='Message Count',
            titleside='right',
            thickness=15,
            len=0.75,
            tickfont=dict(size=12),
            titlefont=dict(size=14)
        ),
        hovertemplate='Day: %{y}<br>Time: %{x}<br>Messages: %{z}<extra></extra>'
    ))
    
    # Update layout for the second figure with broader display
    figure2.update_layout(
        title=dict(
            text='Detailed Weekly Activity Pattern',
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
        width=1400,  # Increased width
        height=700   # Increased height
    )
    
    return user_heatmap, figure1, figure2

def calculate_response_times(df):
    """Calculate response times between messages for each user"""
    df = df.copy()
    df = df[df['user'] != 'group_notification']
    
    # Convert date to datetime if it's not already
    df['date'] = pd.to_datetime(df['date'])
    
    # Sort by date
    df = df.sort_values('date')
    
    # Calculate time difference between consecutive messages
    df['prev_msg_time'] = df['date'].shift()
    df['prev_msg_user'] = df['user'].shift()
    
    # Calculate response time only when it's a different user
    df['response_time'] = None
    different_user_mask = df['user'] != df['prev_msg_user']
    df.loc[different_user_mask, 'response_time'] = (
        df.loc[different_user_mask, 'date'] - 
        df.loc[different_user_mask, 'prev_msg_time']
    ).dt.total_seconds() / 60  # Convert to minutes
    
    # Filter out responses longer than 24 hours (considered new conversations)
    df = df[df['response_time'] <= 24 * 60]
    
    return df

def analyze_response_patterns(df, selected_user='Overall'):
    """Analyze response patterns for users"""
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    # Calculate average response times for each user
    response_stats = df.groupby('user')['response_time'].agg([
        ('avg_response_time', 'mean'),
        ('min_response_time', 'min'),
        ('max_response_time', 'max'),
        ('response_count', 'count')
    ]).round(2)
    
    return response_stats
