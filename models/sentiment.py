# =============================================
# SECTION 1: IMPORTS AND INITIALIZATION
# =============================================
import pandas as pd
import numpy as np
import re
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from textblob import TextBlob
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import time
from functools import lru_cache

# Initialize sentiment analyzer with error handling and caching
@st.cache_resource(show_spinner=False)
def initialize_sentiment_analyzer():
    """
    Initialize the VADER sentiment analyzer
    
    Returns:
    --------
    SentimentIntensityAnalyzer
        Initialized sentiment analyzer or None if failed
    """
    try:
        # Check if vader_lexicon is available
        nltk.data.find('sentiment/vader_lexicon.zip')
        return SentimentIntensityAnalyzer()
    except LookupError:
        try:
            # Download if not available
            with st.spinner('Downloading required NLTK sentiment data...'):
                nltk.download('vader_lexicon', quiet=True)
            return SentimentIntensityAnalyzer()
        except Exception as e:
            st.warning("Could not initialize NLTK's VADER sentiment analyzer. Using TextBlob only.")
            return None

# Initialize stopwords for word clouds
stop_words = set(STOPWORDS)
custom_stopwords = [
    'media', 'omitted', 'https', 'http', 'www', 'com', 'message', 'deleted', 
    'ha', 'le', 'ki', 'ke', 'hi', 'me', 'ki', 'bhi', 'ko', 'hai', 'ho'
]
stop_words.update(custom_stopwords)

# =============================================
# SECTION 2: TEXT PREPROCESSING
# =============================================

# Use caching for expensive text cleaning operations
@lru_cache(maxsize=1024)
def clean_text(text):
    """
    Clean text for sentiment analysis
    
    Parameters:
    -----------
    text : str
        Input text to clean
        
    Returns:
    --------
    str
        Cleaned text
    """
    if not isinstance(text, str):
        return ""
        
    # Remove URLs
    text = re.sub(r'http\S+', '', text)
    
    # Remove special characters but keep emoticons and punctuation for sentiment
    text = re.sub(r'[^\w\s,.!?:;()\'"-]', ' ', text)
    
    # Remove multiple spaces
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

# =============================================
# SECTION 3: SENTIMENT ANALYSIS FUNCTIONS
# =============================================

# Cache individual sentiment scores for reuse
@lru_cache(maxsize=2048)
def get_sentiment_score(text):
    """
    Get sentiment score for a text using VADER and TextBlob
    
    Parameters:
    -----------
    text : str
        Text to analyze
        
    Returns:
    --------
    float
        Sentiment score between -1 (negative) and 1 (positive)
    """
    if not text or text == '<Media omitted>\n':
        return 0
    
    # Get clean text
    clean = clean_text(text)
    if not clean:
        return 0
    
    # Use VADER if available
    analyzer = initialize_sentiment_analyzer()
    if analyzer:
        try:
            # VADER returns compound score between -1 and 1
            score = analyzer.polarity_scores(clean)['compound']
        except Exception:
            # Fallback to TextBlob
            score = TextBlob(clean).sentiment.polarity
    else:
        # Use TextBlob directly
        score = TextBlob(clean).sentiment.polarity
    
    return score


def get_sentiment_category(score):
    """
    Convert sentiment score to category
    
    Parameters:
    -----------
    score : float
        Sentiment score between -1 (negative) and 1 (positive)
        
    Returns:
    --------
    str
        Sentiment category: 'Positive', 'Negative', or 'Neutral'
    """
    if score > 0.1:
        return 'Positive'
    elif score < -0.1:
        return 'Negative'
    else:
        return 'Neutral'


def analyze_sentiment(df, selected_user='Overall'):
    """
    Analyze sentiment for all messages in dataframe
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Preprocessed chat dataframe
    selected_user : str
        User to filter by or 'Overall' for all users
        
    Returns:
    --------
    pandas.DataFrame
        Original dataframe with sentiment scores and categories added
    """
    start_time = time.time()
    
    # Filter by user if needed
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    # Filter out system notifications
    df = df[df['user'] != 'group_notification']
    
    # Create a copy to avoid modifying the original
    sentiment_df = df.copy()
    
    # Show progress indicator
    total_messages = len(sentiment_df)
    progress_text = st.empty()
    progress_bar = st.progress(0)
    
    if total_messages > 100:
        progress_text.text(f"Analyzing sentiment for {total_messages} messages...")
    
    # Process in batches for better performance
    batch_size = 100
    num_batches = (total_messages + batch_size - 1) // batch_size
    
    # Pre-allocate sentiment score array for better performance
    sentiment_scores = np.zeros(total_messages)
    
    # Process in batches
    for i in range(num_batches):
        start_idx = i * batch_size
        end_idx = min((i + 1) * batch_size, total_messages)
        
        # Process batch
        for j in range(start_idx, end_idx):
            sentiment_scores[j] = get_sentiment_score(sentiment_df.iloc[j]['message'])
        
        # Update progress every batch
        if total_messages > 100:
            progress_bar.progress((i + 1) / num_batches)
    
    # Assign scores to dataframe
    sentiment_df['sentiment_score'] = sentiment_scores
    sentiment_df['sentiment'] = sentiment_df['sentiment_score'].apply(get_sentiment_category)
    
    # Clean up progress indicators
    if total_messages > 100:
        elapsed_time = time.time() - start_time
        progress_text.text(f"Sentiment analysis completed in {elapsed_time:.2f} seconds")
        time.sleep(1)  # Give a moment to read the completion message
        progress_text.empty()
        progress_bar.empty()
    
    return sentiment_df

# Add cache for sentiment stats to improve UI responsiveness
@st.cache_data(ttl=600)
def get_sentiment_stats(sentiment_df):
    """
    Get sentiment statistics from analyzed dataframe
    
    Parameters:
    -----------
    sentiment_df : pandas.DataFrame
        Dataframe with sentiment analysis results
        
    Returns:
    --------
    dict
        Dictionary with percentage of each sentiment category
    """
    # Count messages by sentiment
    sentiment_counts = sentiment_df['sentiment'].value_counts()
    total = len(sentiment_df)
    
    # Calculate percentages
    sentiment_stats = {}
    for category in ['Positive', 'Negative', 'Neutral']:
        count = sentiment_counts.get(category, 0)
        sentiment_stats[category] = (count / total * 100) if total > 0 else 0
    
    return sentiment_stats

# =============================================
# SECTION 4: VISUALIZATION FUNCTIONS
# =============================================

# Cache visualization to prevent recalculation
@st.cache_data(ttl=600)
def plot_sentiment_pie(sentiment_stats):
    """
    Create pie chart of sentiment distribution
    
    Parameters:
    -----------
    sentiment_stats : dict
        Dictionary with percentage of each sentiment category
        
    Returns:
    --------
    plotly.graph_objects.Figure
        Interactive pie chart
    """
    # Extract data
    labels = list(sentiment_stats.keys())
    values = list(sentiment_stats.values())
    
    # Custom colors
    colors = ['#4CAF50', '#F44336', '#3F51B5']  # Green, Red, Blue
    
    # Create pie chart
    fig = px.pie(
        values=values,
        names=labels,
        title='Message Sentiment Distribution',
        color_discrete_sequence=colors
    )
    
    # Update layout
    fig.update_traces(
        textinfo='percent+label',
        pull=[0.05, 0.05, 0.05],
        marker=dict(line=dict(color='#1f2937', width=1))
    )
    
    return fig

# Cache trend visualization
@st.cache_data(ttl=600)
def plot_sentiment_trend(sentiment_df):
    """
    Create line chart of sentiment trend over time
    
    Parameters:
    -----------
    sentiment_df : pandas.DataFrame
        Dataframe with sentiment analysis results
        
    Returns:
    --------
    plotly.graph_objects.Figure
        Interactive line chart
    """
    # Prepare data
    sentiment_df['date'] = pd.to_datetime(sentiment_df['only_date'])
    
    # Group by date and calculate average sentiment
    daily_sentiment = sentiment_df.groupby('date').agg({
        'sentiment_score': 'mean',
        'message': 'count'
    }).reset_index()
    
    # Add 7-day moving average
    daily_sentiment['sentiment_ma'] = daily_sentiment['sentiment_score'].rolling(window=7, min_periods=1).mean()
    
    # Create the figure
    fig = go.Figure()
    
    # Add scatter plot of daily sentiment
    fig.add_trace(go.Scatter(
        x=daily_sentiment['date'],
        y=daily_sentiment['sentiment_score'],
        mode='markers',
        name='Daily Sentiment',
        marker=dict(
            size=8, 
            color=daily_sentiment['sentiment_score'],
            colorscale=[
                [0, '#F44336'],      # Red for negative
                [0.5, '#3F51B5'],    # Blue for neutral
                [1, '#4CAF50']       # Green for positive
            ],
            colorbar=dict(title='Sentiment Score'),
            showscale=True
        )
    ))
    
    # Add 7-day moving average line
    fig.add_trace(go.Scatter(
        x=daily_sentiment['date'],
        y=daily_sentiment['sentiment_ma'],
        mode='lines',
        name='7-day Moving Average',
        line=dict(color='#FF9800', width=2)
    ))
    
    # Add reference lines
    fig.add_shape(
        type="line",
        x0=daily_sentiment['date'].min(),
        y0=0,
        x1=daily_sentiment['date'].max(),
        y1=0,
        line=dict(color="#6c757d", dash="dash", width=1)
    )
    
    # Update layout
    fig.update_layout(
        title='Sentiment Trend Over Time',
        xaxis_title='Date',
        yaxis_title='Sentiment Score',
        yaxis=dict(
            range=[-1.1, 1.1],
            tickvals=[-1, -0.5, 0, 0.5, 1],
            ticktext=['Very Negative', 'Negative', 'Neutral', 'Positive', 'Very Positive']
        ),
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        ),
        hovermode='x unified'
    )
    
    return fig

# Cache wordcloud generation
@st.cache_data(ttl=600)
def generate_sentiment_wordclouds(sentiment_df):
    """
    Generate word clouds for each sentiment category
    
    Parameters:
    -----------
    sentiment_df : pandas.DataFrame
        Dataframe with sentiment analysis results
        
    Returns:
    --------
    tuple
        Three WordCloud objects (positive, negative, neutral)
    """
    # Configure word cloud settings
    def create_wordcloud(text, colormap):
        if not text:
            return None
        
        return WordCloud(
            width=800,
            height=400,
            background_color='black',
            stopwords=stop_words,
            max_words=200,
            min_font_size=5,
            max_font_size=100,
            colormap=colormap,
            collocations=True,
            normalize_plurals=True,
            contour_width=1,
            contour_color='#4b5563'
        ).generate(text)
    
    # Create text for each sentiment
    positive_text = ' '.join(sentiment_df[sentiment_df['sentiment'] == 'Positive']['message'].astype(str))
    negative_text = ' '.join(sentiment_df[sentiment_df['sentiment'] == 'Negative']['message'].astype(str))
    neutral_text = ' '.join(sentiment_df[sentiment_df['sentiment'] == 'Neutral']['message'].astype(str))
    
    # Create word clouds with different color schemes
    pos_wc = create_wordcloud(positive_text, 'Greens')
    neg_wc = create_wordcloud(negative_text, 'Reds')
    neu_wc = create_wordcloud(neutral_text, 'Blues')
    
    return pos_wc, neg_wc, neu_wc