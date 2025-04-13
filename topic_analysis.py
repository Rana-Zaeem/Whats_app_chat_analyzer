# SECTION 1: Imports and NLTK Setup
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re
import streamlit as st

# Initialize NLTK with error handling
def ensure_nltk_data():
    """Initialize required NLTK data with fallback options"""
    try:
        nltk.data.find('tokenizers/punkt')
        nltk.data.find('corpora/stopwords')
    except LookupError:
        try:
            with st.spinner('Downloading required NLTK data...'):
                nltk.download('punkt', quiet=True)
                nltk.download('stopwords', quiet=True)
            return True
        except Exception as e:
            st.warning("NLTK data download failed, using simple tokenization instead")
            return False

def simple_tokenize(text):
    """Simple fallback tokenizer when NLTK is unavailable"""
    return text.split()

# SECTION 2: Topic Categories Definition
# Predefined topic categories and their related words
PREDEFINED_TOPICS = {
    'Deleted Messages': [
        'deleted', 'message', 'edited', 'copy', 'haie',
        'remove', 'clear', 'gone', 'missing', 'erased',
        'unsend', 'recall', 'undo', 'correction', 'mistake'
    ],
    'Class Discussions': [
        'class', 'makeup', 'make', 'slot', 'asslam',
        'lecture', 'assignment', 'quiz', 'exam', 'study',
        'teacher', 'subject', 'course', 'semester', 'notes',
        'homework', 'project', 'deadline', 'submission', 'tutorial'
    ],
    'Group Management': [
        'group', 'send', 'link', 'join', 'whatsapp',
        'admin', 'add', 'remove', 'member', 'invite',
        'welcome', 'left', 'added', 'shared', 'forward',
        'rules', 'guidelines', 'broadcast', 'announcement', 'notice'
    ],
    'Future Planning': [
        'null', 'verify', 'apka', 'degree', 'future',
        'plan', 'career', 'job', 'opportunity', 'interview',
        'resume', 'cv', 'position', 'application', 'work',
        'internship', 'placement', 'company', 'salary', 'offer'
    ],
    'Greetings & Wishes': [
        'ameen', 'allah', 'mubarak', 'khair', 'salam',
        'jazakallah', 'inshallah', 'alhamdulillah', 'mashallah',
        'thanks', 'welcome', 'regards', 'bye', 'hello', 'hi',
        'good morning', 'good night', 'eid', 'ramadan', 'jummah'
    ],
    'Assignment Help': [
        'help', 'solution', 'answer', 'solve', 'explain',
        'question', 'problem', 'understand', 'clarify', 'doubt',
        'confusion', 'homework', 'assignment', 'due', 'task'
    ],
    'Technical Issues': [
        'error', 'problem', 'issue', 'bug', 'crash',
        'not working', 'failed', 'fix', 'solved', 'update',
        'internet', 'connection', 'network', 'wifi', 'mobile'
    ],
    'Schedule Coordination': [
        'time', 'schedule', 'when', 'tomorrow', 'today',
        'meeting', 'class', 'session', 'timing', 'date',
        'morning', 'afternoon', 'evening', 'night', 'weekend'
    ],
    'File Sharing': [
        'file', 'document', 'pdf', 'image', 'video',
        'share', 'upload', 'download', 'sent', 'receive',
        'attachment', 'folder', 'zip', 'screenshot', 'photo'
    ],
    'Events & Activities': [
        'event', 'activity', 'seminar', 'workshop', 'conference',
        'meeting', 'gathering', 'celebration', 'party', 'function',
        'ceremony', 'program', 'festival', 'competition', 'show'
    ],
    'Study Materials': [
        'book', 'notes', 'slides', 'presentation', 'material',
        'reference', 'resource', 'guide', 'textbook', 'handout',
        'lecture', 'chapter', 'topic', 'course', 'syllabus'
    ],
    'Exam Preparations': [
        'exam', 'test', 'quiz', 'preparation', 'study',
        'revision', 'practice', 'question paper', 'past paper', 'mcqs',
        'final', 'midterm', 'viva', 'oral', 'written'
    ],
    'Project Discussions': [
        'project', 'team', 'group', 'work', 'task',
        'deadline', 'progress', 'update', 'status', 'report',
        'collaboration', 'contribution', 'responsibility', 'role', 'plan'
    ],
    'Sports & Games': [
        'match', 'game', 'play', 'team', 'win',
        'cricket', 'football', 'score', 'tournament', 'player',
        'sports', 'competition', 'championship', 'league', 'result'
    ],
    'Food & Dining': [
        'food', 'lunch', 'dinner', 'breakfast', 'meal',
        'restaurant', 'cafe', 'order', 'menu', 'eat',
        'hungry', 'snack', 'drink', 'delivery', 'taste'
    ],
    'Transport & Travel': [
        'bus', 'car', 'ride', 'transport', 'travel',
        'pickup', 'drop', 'location', 'route', 'way',
        'traffic', 'late', 'early', 'reach', 'station'
    ],
    'Birthday Wishes': [
        'birthday', 'happy', 'wish', 'celebration', 'party',
        'cake', 'gift', 'surprise', 'bless', 'congratulations',
        'anniversary', 'special day', 'celebration', 'wishes', 'joy'
    ],
    'Weather Updates': [
        'weather', 'rain', 'sunny', 'hot', 'cold',
        'temperature', 'climate', 'forecast', 'storm', 'wind',
        'umbrella', 'weather report', 'cloudy', 'humidity', 'season'
    ],
    'Health & Wellness': [
        'health', 'sick', 'medicine', 'doctor', 'hospital',
        'treatment', 'rest', 'recover', 'feeling', 'symptoms',
        'covid', 'virus', 'fever', 'flu', 'vaccine'
    ],
    'Music & Entertainment': [
        'song', 'music', 'movie', 'show', 'concert',
        'artist', 'album', 'release', 'watch', 'listen',
        'playlist', 'video', 'entertainment', 'performance', 'live'
    ],
    'Social Events': [
        'party', 'gathering', 'meet', 'hangout', 'social',
        'friends', 'group', 'plan', 'weekend', 'outing',
        'picnic', 'trip', 'celebration', 'get together', 'reunion'
    ],
    'Prayer Times': [
        'prayer', 'namaz', 'salah', 'time', 'mosque',
        'fajr', 'zuhr', 'asr', 'maghrib', 'isha',
        'juma', 'quran', 'dua', 'ibadat', 'masjid'
    ],
    'Hostel Life': [
        'hostel', 'room', 'roommate', 'mess', 'warden',
        'accommodation', 'staying', 'facility', 'complaint', 'maintenance',
        'rent', 'utility', 'cleaning', 'rules', 'timing'
    ],
    'Society Activities': [
        'society', 'club', 'member', 'meeting', 'activity',
        'position', 'election', 'committee', 'responsibility', 'event',
        'initiative', 'volunteer', 'participation', 'organization', 'team'
    ],
    'Financial Matters': [
        'fee', 'payment', 'money', 'dues', 'amount',
        'pay', 'paid', 'receipt', 'account', 'transaction',
        'deadline', 'scholarship', 'fund', 'expense', 'budget'
    ],
    'Library Resources': [
        'library', 'book', 'borrow', 'return', 'due',
        'fine', 'reference', 'card', 'membership', 'access',
        'catalogue', 'journal', 'magazine', 'research', 'study'
    ],
    'Sports Events': [
        'tournament', 'match', 'game', 'team', 'player',
        'competition', 'sport', 'practice', 'training', 'coach',
        'ground', 'field', 'equipment', 'schedule', 'result'
    ],
    'Lab Work': [
        'lab', 'experiment', 'practical', 'equipment', 'report',
        'observation', 'procedure', 'result', 'submission', 'partner',
        'manual', 'safety', 'demonstration', 'preparation', 'data'
    ],
    'Research Activities': [
        'research', 'paper', 'publication', 'journal', 'conference',
        'study', 'analysis', 'data', 'methodology', 'literature',
        'review', 'survey', 'finding', 'conclusion', 'reference'
    ],
    'Part-time Work': [
        'job', 'work', 'part-time', 'earning', 'salary',
        'timing', 'schedule', 'shift', 'payment', 'experience',
        'application', 'interview', 'position', 'opportunity', 'vacancy'
    ],
    'Cultural Events': [
        'culture', 'festival', 'celebration', 'tradition', 'event',
        'performance', 'dance', 'music', 'art', 'exhibition',
        'show', 'competition', 'talent', 'cultural night', 'program'
    ],
    'Academic Awards': [
        'award', 'prize', 'achievement', 'recognition', 'ceremony',
        'medal', 'certificate', 'honor', 'distinction', 'merit',
        'scholarship', 'performance', 'excellence', 'appreciation', 'winner'
    ],
    'Personal Problems': [
        'problem', 'issue', 'help', 'advice', 'support',
        'difficulty', 'situation', 'worry', 'concern', 'stress',
        'anxiety', 'depression', 'pressure', 'mental health', 'counseling'
    ]
}

# SECTION 3: Text Processing Functions
def preprocess_text(text):
    """Clean and preprocess text for topic modeling"""
    # Convert to lowercase
    text = text.lower()
    
    # Remove special characters and digits
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)
    
    # Tokenize with fallback
    try:
        if ensure_nltk_data():
            tokens = word_tokenize(text)
        else:
            tokens = simple_tokenize(text)
    except Exception:
        tokens = simple_tokenize(text)
    
    # Handle stopwords with fallback
    try:
        stop_words = set(stopwords.words('english'))
    except:
        stop_words = {'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves'}
    
    # Add custom stopwords
    try:
        with open('stop_hinglish.txt', 'r') as f:
            custom_stops = set(f.read().split())
        stop_words.update(custom_stops)
    except:
        pass
    
    tokens = [token for token in tokens if token not in stop_words and len(token) > 2]
    return ' '.join(tokens)

# SECTION 4: Topic Analysis Functions
def calculate_topic_scores(text, topic_words):
    """Calculate how well a text matches a predefined topic"""
    text = text.lower()
    score = sum(1 for word in topic_words if word.lower() in text)
    return score

def classify_message(message, predefined_topics=PREDEFINED_TOPICS):
    """Classify a single message into predefined topics"""
    processed_message = preprocess_text(message)
    scores = {}
    
    for topic, keywords in predefined_topics.items():
        score = calculate_topic_scores(processed_message, keywords)
        scores[topic] = score
    
    return scores

def extract_topics(df, selected_user='Overall', num_topics=5, num_words=5):
    """Extract main topics from chat messages with predefined categories"""
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    # Filter messages
    df = df[df['message'] != '<Media omitted>\n']
    df = df[df['user'] != 'group_notification']
    
    # Calculate topic scores
    topic_scores = []
    for message in df['message']:
        scores = classify_message(message)
        topic_scores.append(scores)
    
    # Process results
    topic_scores_df = pd.DataFrame(topic_scores)
    total_messages = len(df)
    topic_strengths = {}
    
    for topic in PREDEFINED_TOPICS.keys():
        topic_count = sum(1 for score in topic_scores if score[topic] > 0)
        strength = (topic_count / total_messages * 100) if total_messages > 0 else 0
        topic_strengths[topic] = strength
    
    # Create output DataFrame
    topics = []
    for topic, strength in topic_strengths.items():
        topics.append({
            'topic_id': len(topics) + 1,
            'topic_name': topic,
            'top_words': ', '.join(PREDEFINED_TOPICS[topic][:5]),
            'strength': strength,
            'strength_percent': round(strength, 2)
        })
    
    topics_df = pd.DataFrame(topics)
    return topics_df.sort_values('strength', ascending=False)

# SECTION 5: Visualization Functions
def create_topic_visualization(topics_df):
    """Create an interactive visualization for topic analysis"""
    import plotly.graph_objects as go
    
    if topics_df is None or len(topics_df) == 0:
        return None
    
    # Create bar chart
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=topics_df['topic_name'],
        y=topics_df['strength_percent'],
        text=topics_df['strength_percent'].apply(lambda x: f'{x:.1f}%'),
        textposition='auto',
        marker_color=[
            '#2563eb',  # Blue for Deleted Messages
            '#10b981',  # Green for Class Discussions
            '#f59e0b',  # Amber for Group Management
            '#8b5cf6',  # Purple for Future Planning
            '#ef4444',  # Red for Greetings & Wishes
        ],
        hovertext=topics_df['top_words'],
        hovertemplate="<b>%{x}</b><br>" +
                     "Prevalence: %{text}<br>" +
                     "Top words: %{hovertext}<br>" +
                     "<extra></extra>"
    ))
    
    # Update layout with professional styling
    fig.update_layout(
        title=dict(
            text='Message Categories Distribution',
            x=0.5,
            y=0.95,
            xanchor='center',
            yanchor='top',
            font=dict(size=24, color='white', family='Arial Black')
        ),
        xaxis_title="Topic Category",
        yaxis_title="Topic Prevalence (%)",
        template='plotly_dark',
        paper_bgcolor='#1f2937',
        plot_bgcolor='#1f2937',
        xaxis=dict(
            tickangle=45,
            tickfont=dict(size=12, color='white'),
            gridcolor='rgba(255, 255, 255, 0.1)',
            linecolor='white'
        ),
        yaxis=dict(
            tickfont=dict(size=12, color='white'),
            gridcolor='rgba(255, 255, 255, 0.1)',
            linecolor='white'
        ),
        margin=dict(l=60, r=60, t=80, b=120),
        width=1000,
        height=600
    )
    
    return fig