import streamlit as st
import time
import pandas as pd
import hashlib

# =============================================
# SECTION 1: IMPORTS AND INITIALIZATION
# =============================================

# Import core data processing modules
from models.preprocessor import preprocess
from models.helper import fetch_stats, busiest_persons, create_word_cloud, most_common_words
from models.helper import emoji_analysis, timeline, daily_timeline, daily_activeness, montly_activeness
from models.helper import activity_heatmap, calculate_response_times, analyze_response_patterns
from models.sentiment import analyze_sentiment, get_sentiment_stats, plot_sentiment_pie
from models.sentiment import plot_sentiment_trend, generate_sentiment_wordclouds
from models.topic_analysis import extract_topics, create_topic_visualization

# Import all component modules
from components.theme_manager import initialize_theme, apply_theme_css, get_theme_colors
from components.styling import apply_custom_css, apply_plotly_config
from components.ui_components import show_splash_screen, show_welcome_screen, show_future_features
from components.sidebar import setup_sidebar
from components.chat_analysis import run_chat_analysis
from components.sentiment_analysis import run_sentiment_analysis
from components.topic_analysis import run_topic_analysis
from components.time_comparison import run_time_comparison

# =============================================
# SECTION 2: STREAMLIT CONFIGURATION
# =============================================

# Must be the first Streamlit command
st.set_page_config(
    page_title="WhatsApp Chat Analyzer",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================
# SECTION 3: UI SETUP AND STYLING
# =============================================

# Import responsive functions first to apply styles
from models.responsive_functions import apply_responsive_styles

# Apply responsive styles
apply_responsive_styles()

# Show guidelines by default when the app starts
if 'show_guidelines' not in st.session_state:
    st.session_state.show_guidelines = True
    # Initialize first_load to True on first run
    st.session_state.first_load = True

# Initialize theme if not already set
initialize_theme()

# Apply theme CSS
apply_theme_css()

# Apply custom CSS styling
apply_custom_css()

# Get current theme
current_theme = get_theme_colors()

# =============================================
# SECTION 4: USER INTERFACE RENDERING
# =============================================

# Display splash screen for first-time visitors
show_splash_screen(current_theme)

# Setup sidebar and get user selections
sidebar_data = setup_sidebar()
show_future = sidebar_data['show_future']
analysis_type = sidebar_data['analysis_type']
uploaded_file = sidebar_data['uploaded_file']

# Show future features if button clicked
if show_future:
    show_future_features()

# =============================================
# SECTION 5: FILE PROCESSING AND ANALYSIS
# =============================================

# Display a welcome screen when no file is uploaded
if uploaded_file is None:
    show_welcome_screen()
else:
    try:
        # Try different encodings to read the file
        encodings = ['utf-8', 'latin1', 'iso-8859-1', 'cp1252']
        data = None
        
        for encoding in encodings:
            try:
                bytes_data = uploaded_file.getvalue()
                data = bytes_data.decode(encoding)
                break
            except UnicodeDecodeError:
                continue
                
        if data is None:
            st.error("Unable to read the file. Please ensure it's a valid WhatsApp chat export.")
            st.stop()
            
        # Process the data
        df = preprocess(data)
        if df is None:
            st.error("Error processing the chat file. Please ensure it's a valid WhatsApp chat export.")
            st.stop()
            
        # Fetch unique user list
        user_list = df['user'].unique().tolist()
        if 'group_notification' in user_list:
            user_list.remove('group_notification')
        user_list.sort()
        user_list.insert(0, 'Overall')
        selected_user = st.sidebar.selectbox('Show Analysis wrt', user_list)

        # =============================================
        # SECTION 6: ADAPTER PATTERN IMPLEMENTATION
        # =============================================
        
        # Create helper, sentiment, and topic_analysis adapters for components
        class HelperAdapter:
            def fetch_stats(self, selected_user, df):
                return fetch_stats(selected_user, df)
                
            def busiest_persons(self, df):
                return busiest_persons(df)
                
            def create_word_cloud(self, selected_user, df):
                return create_word_cloud(selected_user, df)
                
            def most_common_words(self, selected_user, df):
                return most_common_words(selected_user, df)
                
            def emoji_analysis(self, selected_user, df):
                return emoji_analysis(selected_user, df)
                
            def timeline(self, selected_user, df):
                return timeline(selected_user, df)
                
            def daily_timeline(self, selected_user, df):
                return daily_timeline(selected_user, df)
                
            def daily_activeness(self, selected_user, df):
                return daily_activeness(selected_user, df)
                
            def montly_activeness(self, selected_user, df):
                return montly_activeness(selected_user, df)
                
            def activity_heatmap(self, selected_user, df):
                return activity_heatmap(selected_user, df)
                
            def calculate_response_times(self, df):
                return calculate_response_times(df)
                
            def analyze_response_patterns(self, df_with_response, selected_user):
                return analyze_response_patterns(df_with_response, selected_user)
        
        class SentimentAdapter:
            def analyze_sentiment(self, df, selected_user):
                return analyze_sentiment(df, selected_user)
                
            def get_sentiment_stats(self, sentiment_df):
                return get_sentiment_stats(sentiment_df)
                
            def plot_sentiment_pie(self, sentiment_stats):
                return plot_sentiment_pie(sentiment_stats)
                
            def plot_sentiment_trend(self, sentiment_df):
                return plot_sentiment_trend(sentiment_df)
                
            def generate_sentiment_wordclouds(self, sentiment_df):
                return generate_sentiment_wordclouds(sentiment_df)
                
        class TopicAnalysisAdapter:
            def extract_topics(self, df, selected_user):
                return extract_topics(df, selected_user)
                
            def create_topic_visualization(self, topics_df):
                return create_topic_visualization(topics_df)
        
        # =============================================
        # SECTION 7: ANALYSIS ROUTING
        # =============================================
        
        # Create adapter instances
        helper_adapter = HelperAdapter()
        sentiment_adapter = SentimentAdapter()
        topic_analysis_adapter = TopicAnalysisAdapter()
        
        # Route to the appropriate analysis module based on user selection
        if analysis_type == "Chat Analysis":
            run_chat_analysis(selected_user, df, helper_adapter)
        elif analysis_type == "Sentiment Analysis":
            run_sentiment_analysis(selected_user, df, sentiment_adapter)
        elif analysis_type == "Topic Analysis":
            run_topic_analysis(selected_user, df, topic_analysis_adapter)
        elif analysis_type == "Time Comparison":
            run_time_comparison(selected_user, df)

    except Exception as e:
        # Show error message and stop execution
        st.error(f"An error occurred: {str(e)}")
        st.stop()

# =============================================
# SECTION 8: ENHANCED INTERACTIVITY
# =============================================

# Apply Plotly configuration for better interactivity
apply_plotly_config()
