# =============================================
# SECTION 1: IMPORTS AND NLTK SETUP
# =============================================
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re
import streamlit as st
import plotly.express as px
import time
from functools import lru_cache

# Initialize NLTK with error handling and caching
@st.cache_resource(show_spinner=False)
def ensure_nltk_data():
    """
    Initialize required NLTK data with fallback options
    
    Returns:
    --------
    bool
        True if NLTK data is available, False otherwise
    """
    try:
        nltk.data.find('tokenizers/punkt')
        nltk.data.find('corpora/stopwords')
        return True
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
    """
    Simple fallback tokenizer when NLTK is unavailable
    
    Parameters:
    -----------
    text : str
        Input text to tokenize
        
    Returns:
    --------
    list
        List of tokens
    """
    return text.split()

# =============================================
# SECTION 2: TOPIC CATEGORIES DEFINITION
# =============================================

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
        'disease', 'cure', 'prescription', 'medical', 'illness'
    ],
    'Hostel Affairs': [
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

# =============================================
# SECTION 3: TEXT PROCESSING FUNCTIONS
# =============================================

# Use caching for repeated text preprocessing
@lru_cache(maxsize=1024)
def preprocess_text(text):
    """
    Clean and preprocess text for topic modeling
    
    Parameters:
    -----------
    text : str
        Input text to preprocess
        
    Returns:
    --------
    str
        Preprocessed text
    """
    # Check for empty or invalid input
    if not text or not isinstance(text, str):
        return ""
        
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

# =============================================
# SECTION 4: TOPIC ANALYSIS FUNCTIONS
# =============================================

# Cache topic score calculations for better performance
@lru_cache(maxsize=1024)
def calculate_topic_scores(text, topic_words_tuple):
    """
    Calculate how well a text matches a predefined topic
    
    Parameters:
    -----------
    text : str
        Input text to analyze
    topic_words_tuple : tuple
        Tuple of words that define a topic (converted from list for cache compatibility)
        
    Returns:
    --------
    float
        Score representing how well the text matches the topic
    """
    # Skip empty or invalid texts
    if not text or not isinstance(text, str):
        return 0
    
    # Preprocess the message
    tokens = preprocess_text(text).split()
    if not tokens:
        return 0
    
    # Convert tuple back to list for processing
    topic_words = list(topic_words_tuple)
    
    # Count matches with topic words using vectorized operations where possible
    matches = 0
    for token in tokens:
        for topic_word in topic_words:
            # Full match or partial match for longer words
            if token == topic_word or (len(topic_word) > 4 and token in topic_word):
                matches += 1
                break  # Once a match is found for this token, move to next token
    
    # Return a normalized score
    return matches / len(tokens) if tokens else 0


def classify_message(message, predefined_topics=None):
    """
    Classify a single message into predefined topics
    
    Parameters:
    -----------
    message : str
        Message to classify
    predefined_topics : dict
        Dictionary of predefined topics and their keywords
        
    Returns:
    --------
    dict
        Score for each topic
    """
    if predefined_topics is None:
        predefined_topics = PREDEFINED_TOPICS
    
    scores = {}
    
    for topic, keywords in predefined_topics.items():
        # Convert keywords list to tuple for caching
        keywords_tuple = tuple(keywords)
        score = calculate_topic_scores(message, keywords_tuple)
        scores[topic] = score
    
    return scores


def extract_topics(df, selected_user='Overall', num_topics=5, num_words=5):
    """
    Extract main topics from chat messages with predefined categories
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Preprocessed chat dataframe
    selected_user : str
        User to filter by or 'Overall' for all users
    num_topics : int
        Number of topics to extract
    num_words : int
        Number of words per topic
        
    Returns:
    --------
    pandas.DataFrame
        DataFrame with extracted topics and their strengths
    """
    start_time = time.time()
    
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    # Filter messages
    df = df[df['message'] != '<Media omitted>\n']
    df = df[df['user'] != 'group_notification']
    
    # Setup progress tracking
    total_messages = len(df)
    progress_text = st.empty()
    progress_bar = st.progress(0)
    
    if total_messages > 50:
        progress_text.text(f"Analyzing topics in {total_messages} messages...")
    
    # Calculate topic scores with batching for better performance
    topic_scores = []
    batch_size = 50
    num_batches = (total_messages + batch_size - 1) // batch_size
    
    for i in range(num_batches):
        start_idx = i * batch_size
        end_idx = min((i + 1) * batch_size, total_messages)
        
        # Process batch
        batch_messages = df['message'].iloc[start_idx:end_idx].tolist()
        batch_scores = []
        for message in batch_messages:
            batch_scores.append(classify_message(message))
        
        topic_scores.extend(batch_scores)
        
        # Update progress every batch
        if total_messages > 50:
            progress_bar.progress((i + 1) / num_batches)
    
    # Process results
    topic_strengths = {}
    
    for topic in PREDEFINED_TOPICS.keys():
        # Count messages with any mention of this topic
        topic_count = sum(1 for score in topic_scores if score.get(topic, 0) > 0)
        strength = (topic_count / total_messages * 100) if total_messages > 0 else 0
        topic_strengths[topic] = strength
    
    # Create output DataFrame
    topics = []
    for topic, strength in topic_strengths.items():
        # Only include topics that have some presence
        if strength > 0:
            topics.append({
                'topic_id': len(topics) + 1,
                'topic_name': topic,
                'top_words': ', '.join(PREDEFINED_TOPICS[topic][:5]),
                'strength': strength,
                'strength_percent': round(strength, 2)
            })
    
    # Clean up progress indicators
    if total_messages > 50:
        elapsed_time = time.time() - start_time
        progress_text.text(f"Topic analysis completed in {elapsed_time:.2f} seconds")
        time.sleep(1)  # Give a moment to read the completion message
        progress_text.empty()
        progress_bar.empty()
    
    topics_df = pd.DataFrame(topics)
    return topics_df.sort_values('strength', ascending=False)

# =============================================
# SECTION 5: VISUALIZATION FUNCTIONS
# =============================================

# Cache visualization to prevent recalculation
@st.cache_data(ttl=600)
def create_topic_visualization(topics_df):
    """
    Create an interactive visualization for topic analysis
    
    Parameters:
    -----------
    topics_df : pandas.DataFrame
        DataFrame with topic information
        
    Returns:
    --------
    plotly.graph_objects.Figure
        Interactive visualization of topics
    """
    # Filter to non-zero topics only
    topics_df = topics_df[topics_df['strength'] > 0]
    
    if len(topics_df) == 0:
        return None
    
    # Sort for better visualization
    topics_df = topics_df.sort_values('strength', ascending=True)
    
    # Use only top topics for better readability
    if len(topics_df) > 15:
        topics_df = topics_df.tail(15)
    
    # Create horizontal bar chart with enhanced styling
    fig = px.bar(
        topics_df,
        y='topic_name',
        x='strength_percent',
        orientation='h',
        title='Topic Distribution in Conversations',
        labels={'strength_percent': 'Prevalence (%)', 'topic_name': 'Topic'},
        text='strength_percent',
        color='strength_percent',
        color_continuous_scale=px.colors.sequential.Viridis
    )
    
    # Update layout for better appearance
    fig.update_traces(
        texttemplate='%{text:.1f}%',
        textposition='outside'
    )
    
    fig.update_layout(
        yaxis={'categoryorder': 'total ascending'},
        height=500,
        xaxis_title='Topic Strength (%)',
        yaxis_title='Topic Categories',
        coloraxis_showscale=False,
        hoverlabel=dict(
            bgcolor="white",
            font_size=12,
            font_family="Arial"
        )
    )
    
    return fig