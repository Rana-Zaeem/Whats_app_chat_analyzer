from textblob import TextBlob
import pandas as pd
from wordcloud import WordCloud
import plotly.express as px
from collections import defaultdict

# SECTION 1: Configuration Constants
# Common word lists for sentiment filtering
POSITIVE_WORDS = {
    'good', 'great', 'awesome', 'excellent', 'happy', 'love', 'wonderful', 'best',
    'beautiful', 'thanks', 'thank', 'nice', 'well', 'perfect', 'fun', 'exciting',
    'amazing', 'fantastic', 'glad', 'pleasure', 'blessed', 'success', 'enjoy',
    'positive', 'win', 'winning', 'congratulations', 'congrats', 'helpful'
}

NEGATIVE_WORDS = {
    'bad', 'worst', 'terrible', 'awful', 'hate', 'sad', 'poor', 'wrong',
    'horrible', 'sorry', 'fail', 'failed', 'disappointed', 'disappointing',
    'useless', 'waste', 'problem', 'difficult', 'unfortunately', 'upset',
    'never', 'impossible', 'annoying', 'frustrated', 'frustrating', 'disaster'
}

# SECTION 2: Core Sentiment Analysis Functions
def get_sentiment(text):
    """Calculate sentiment polarity score for a given text"""
    return TextBlob(str(text)).sentiment.polarity

def categorize_sentiment(score):
    """Categorize sentiment score into Positive/Negative/Neutral"""
    if score > 0.05:
        return 'Positive'
    elif score < -0.05:
        return 'Negative'
    else:
        return 'Neutral'

def analyze_sentiment(df, selected_user):
    """Analyze sentiment for messages in the DataFrame"""
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    df['sentiment_score'] = df['message'].apply(get_sentiment)
    df['sentiment_category'] = df['sentiment_score'].apply(categorize_sentiment)
    
    return df

# SECTION 3: Statistical Analysis
def get_sentiment_stats(df):
    """Calculate sentiment distribution statistics"""
    sentiment_counts = df['sentiment_category'].value_counts()
    total = len(df)
    sentiment_percentages = (sentiment_counts / total * 100).round(2)
    return sentiment_percentages

# SECTION 4: Visualization Functions
def plot_sentiment_pie(sentiment_percentages):
    """Create an interactive pie chart of sentiment distribution"""
    fig = px.pie(
        values=sentiment_percentages.values,
        names=sentiment_percentages.index,
        title='Message Sentiment Distribution',
        color_discrete_sequence=['#2ECC71', '#E74C3C', '#3498DB']
    )
    
    fig.update_layout(
        width=800,
        height=500,
        title_x=0.5,
        margin=dict(t=50, l=50, r=50, b=50),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    return fig

def plot_sentiment_trend(df):
    """Create an interactive line plot of sentiment trends over time"""
    df_grouped = df.groupby('only_date')['sentiment_score'].mean().reset_index()
    fig = px.line(
        df_grouped, 
        x='only_date', 
        y='sentiment_score',
        title='Sentiment Trend Over Time'
    )
    
    fig.update_layout(
        width=800,
        height=500,
        title_x=0.5,
        margin=dict(t=50, l=50, r=50, b=50),
        xaxis_title="Date",
        yaxis_title="Average Sentiment Score",
        hovermode='x unified'
    )
    return fig

# SECTION 5: Word Cloud Generation
def generate_sentiment_wordclouds(df):
    """Generate separate word clouds for positive and negative messages"""
    # Configure word cloud settings
    pos_wc = WordCloud(
        width=800,
        height=400,
        min_font_size=15, 
        background_color='white',
        colormap='YlGn',
        prefer_horizontal=0.7
    )
    
    neg_wc = WordCloud(
        width=800,
        height=400,
        min_font_size=15, 
        background_color='black',
        colormap='Reds',
        prefer_horizontal=0.7
    )
    
    # Word frequency calculation
    positive_words = defaultdict(int)
    negative_words = defaultdict(int)
    
    for message, sentiment in zip(df['message'], df['sentiment_score']):
        words = str(message).lower().split()
        for word in words:
            if len(word) > 3:
                if sentiment > 0.05:
                    word_sentiment = TextBlob(word).sentiment.polarity
                    if word in POSITIVE_WORDS or word_sentiment > 0.2:
                        positive_words[word] += 1
                elif sentiment < -0.05:
                    word_sentiment = TextBlob(word).sentiment.polarity
                    if word in NEGATIVE_WORDS or word_sentiment < -0.2:
                        negative_words[word] += 1
    
    # Generate word clouds
    pos_wordcloud = pos_wc.generate_from_frequencies(positive_words) if positive_words else None
    neg_wordcloud = neg_wc.generate_from_frequencies(negative_words) if negative_words else None
    
    return pos_wordcloud, neg_wordcloud