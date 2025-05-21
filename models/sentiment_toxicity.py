"""
sentiment_toxicity.py
---------------------
Automated Group Sentiment & Toxicity Detection for WhatsApp Chat Analyzer
This module is standalone and does NOT interfere with your existing code.
"""

import pandas as pd
from collections import Counter
from textblob import TextBlob
import re

# Simple list of toxic/abusive words (extend as needed)
TOXIC_WORDS = set([
    'stupid', 'idiot', 'hate', 'fool', 'dumb', 'bastard', 'bloody', 'shit', 'fuck', 'bitch', 'moron', 'asshole',
    'chutiya', 'gandu', 'harami', 'madarchod', 'behenchod', 'bakwas', 'pagal', 'suar', 'kutte', 'kamina', 'kameeni'
])

def get_sentiment(text):
    """
    Returns sentiment polarity (-1 to 1) and label for a given text.
    """
    if not text or not isinstance(text, str):
        return 0, 'neutral'
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0.1:
        label = 'positive'
    elif polarity < -0.1:
        label = 'negative'
    else:
        label = 'neutral'
    return polarity, label

def detect_toxicity(text):
    """
    Returns True if text contains toxic/abusive words, else False.
    """
    if not text or not isinstance(text, str):
        return False
    words = set(re.findall(r'\w+', text.lower()))
    return not TOXIC_WORDS.isdisjoint(words)

def user_sentiment_analysis(df):
    """
    Returns DataFrame with per-user average sentiment and counts of positive/negative/neutral messages.
    """
    results = []
    for user, group in df.groupby('user'):
        sentiments = group['message'].apply(lambda x: get_sentiment(x)[0])
        labels = group['message'].apply(lambda x: get_sentiment(x)[1])
        counts = Counter(labels)
        avg_sentiment = sentiments.mean() if not sentiments.empty else 0
        results.append({
            'user': user,
            'avg_sentiment': round(avg_sentiment, 3),
            'positive_msgs': counts.get('positive', 0),
            'neutral_msgs': counts.get('neutral', 0),
            'negative_msgs': counts.get('negative', 0),
            'total_msgs': len(group)
        })
    return pd.DataFrame(results)

def user_toxicity_analysis(df):
    """
    Returns DataFrame with per-user count of toxic messages and toxicity ratio.
    """
    results = []
    for user, group in df.groupby('user'):
        toxic_msgs = group['message'].apply(detect_toxicity)
        toxic_count = toxic_msgs.sum()
        total = len(group)
        results.append({
            'user': user,
            'toxic_msgs': toxic_count,
            'toxicity_ratio': round(toxic_count/total, 3) if total else 0,
            'total_msgs': total
        })
    return pd.DataFrame(results)

def group_sentiment_summary(df):
    """
    Returns overall group sentiment label and average polarity.
    """
    sentiments = df['message'].apply(lambda x: get_sentiment(x)[0])
    avg = sentiments.mean() if not sentiments.empty else 0
    if avg > 0.1:
        label = 'positive'
    elif avg < -0.1:
        label = 'negative'
    else:
        label = 'neutral'
    return {'group_avg_sentiment': round(avg, 3), 'group_sentiment_label': label}

def group_toxicity_summary(df):
    """
    Returns overall group toxicity ratio (fraction of toxic messages).
    """
    toxic_msgs = df['message'].apply(detect_toxicity)
    ratio = toxic_msgs.sum() / len(df) if len(df) else 0
    return {'group_toxicity_ratio': round(ratio, 3), 'total_msgs': len(df)}
