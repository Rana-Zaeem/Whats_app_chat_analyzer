import streamlit as st
import time

# Must be the first Streamlit command
st.set_page_config(
    page_title="WhatsApp Chat Analyzer",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import responsive functions first to apply styles
import responsive_functions

# Apply responsive styles
responsive_functions.apply_responsive_styles()

# Import all other libraries after set_page_config
from wordcloud import WordCloud
import preprocessor
import helper
import sentiment
import topic_analysis
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd

# Show guidelines by default when the app starts
if 'show_guidelines' not in st.session_state:
    st.session_state.show_guidelines = True
    # Initialize first_load to True on first run
    st.session_state.first_load = True

# Initialize theme if not already set
if 'theme' not in st.session_state:
    st.session_state.theme = 'dark_green'  # Default theme

# Define theme colors
themes = {
    'dark_green': {
        'primary': '#4CAF50',
        'secondary': '#3B88C3',
        'accent': '#E6855E',
        'background': '#0e1117',
        'card_bg': '#1f2937',
        'text': '#ffffff'
    },
    'midnight_blue': {
        'primary': '#3B88C3',
        'secondary': '#9C27B0',
        'accent': '#E6855E',
        'background': '#0d1b2a',
        'card_bg': '#1b263b',
        'text': '#e0e1dd'
    },
    'sunset_orange': {
        'primary': '#FF7043',
        'secondary': '#FFA000',
        'accent': '#7E57C2',
        'background': '#1c1c1c',
        'card_bg': '#2c2c2c',
        'text': '#f5f5f5'
    },
    'deep_purple': {
        'primary': '#7E57C2',
        'secondary': '#26A69A',
        'accent': '#EC407A',
        'background': '#10002b',
        'card_bg': '#240046',
        'text': '#e0e0e0'
    }
}

# Get current theme colors
current_theme = themes[st.session_state.theme]

# Apply current theme dynamically through CSS
st.markdown(f"""
<style>
:root {{
    --primary-color: {current_theme['primary']};
    --secondary-color: {current_theme['secondary']};
    --accent-color: {current_theme['accent']};
    --background-color: {current_theme['background']};
    --card-bg-color: {current_theme['card_bg']};
    --text-color: {current_theme['text']};
}}
</style>
""", unsafe_allow_html=True)

# Custom CSS styling - updated for professional look with animations that use CSS variables for theming
st.markdown("""
    <style>
    /* Main container */
    .main {
        background-color: var(--background-color);
        color: var(--text-color);
        animation: gradientBG 15s ease infinite;
        background-size: 200% 200%;
        background-image: linear-gradient(45deg, var(--background-color), color-mix(in srgb, var(--background-color) 80%, var(--primary-color) 20%), var(--background-color));
    }
    
    /* Headers with animation */
    h1 {
        color: var(--primary-color);
        font-weight: 600;
        margin-bottom: 1.5rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid var(--primary-color);
        animation: fadeInDown 0.8s ease-in-out;
    }
    
    h2 {
        color: var(--secondary-color);
        font-weight: 600;
        margin-bottom: 1rem;
        animation: fadeInDown 0.8s ease-in-out 0.1s;
        animation-fill-mode: both;
    }

    h3 {
        color: var(--accent-color);
        font-weight: 600;
        margin-bottom: 0.8rem;
        animation: fadeInDown 0.8s ease-in-out 0.2s;
        animation-fill-mode: both;
    }
    
    /* Essential animations */
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes slideInUp {
        from {
            transform: translateY(20px);
            opacity: 0;
        }
        to {
            transform: translateY(0);
            opacity: 1;
        }
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }

    /* Chart containers with animation */
    .chart-container {
        background-color: var(--card-bg-color);
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        border-left: 4px solid var(--secondary-color);
        transition: all 0.4s ease;
        animation: fadeIn 0.8s ease-in-out;
    }
    
    .chart-container:hover {
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
        transform: translateY(-5px);
        border-left: 4px solid var(--primary-color);
    }

    /* Section cards with enhanced interactions */
    .section-card {
        background-color: var(--card-bg-color);
        border-radius: 0.5rem;
        padding: 1.5rem;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
        animation: fadeIn 0.8s ease-in-out;
        border-left: 4px solid var(--primary-color);
        transition: all 0.3s ease;
    }
    
    .section-card:hover {
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.25);
        transform: translateY(-3px);
    }
    
    /* DataFrames with animation */
    .dataframe {
        background-color: var(--card-bg-color);
        border-radius: 0.5rem;
        border: 1px solid #374151;
        animation: fadeIn 1s ease-in-out;
        transition: all 0.3s ease;
    }
    
    .dataframe:hover {
        border-color: var(--primary-color);
        box-shadow: 0 0 8px rgba(76, 175, 80, 0.4);
    }
    
    /* Metric styling with animations */
    div[data-testid="metric-container"] {
        transition: transform 0.3s ease;
        animation: slideInUp 0.5s ease-out;
    }

    div[data-testid="metric-container"]:hover {
        transform: translateY(-5px);
    }
    
    div[data-testid="stMetricValue"] {
        font-size: 2rem !important;
        font-weight: bold;
        color: var(--primary-color);
        transition: color 0.3s ease;
    }
    
    div[data-testid="stMetricValue"]:hover {
        text-shadow: 0 0 8px rgba(76, 175, 80, 0.3);
    }
    
    div[data-testid="stMetricDelta"] {
        animation: fadeIn 0.8s ease-in-out;
        animation-delay: 0.5s;
        animation-fill-mode: both;
    }
    
    div[data-testid="stMetricLabel"] {
        font-size: 1rem !important;
        animation: fadeIn 0.8s ease-in-out 0.2s;
        animation-fill-mode: both;
    }
    
    /* Sidebar styling with animation */
    .css-1d391kg {
        background-color: var(--card-bg-color);
        animation: slideInLeft 0.5s ease-in-out;
    }
    
    .sidebar .sidebar-content {
        background-color: var(--card-bg-color);
        animation: slideInLeft 0.5s ease-in-out;
    }
    
    /* Buttons with animation */
    .stButton > button {
        background-color: var(--primary-color);
        color: white;
        border: none;
        border-radius: 4px;
        padding: 0.5rem 1rem;
        transition: all 0.3s;
        animation: fadeIn 0.8s ease-in-out;
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button:hover {
        background-color: color-mix(in srgb, var(--primary-color) 90%, white 10%);
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
        transform: translateY(-2px);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    .stButton > button::after {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 5px;
        height: 5px;
        background: rgba(255, 255, 255, 0.5);
        opacity: 0;
        border-radius: 100%;
        transform: scale(1, 1) translate(-50%);
        transform-origin: 50% 50%;
    }
    
    .stButton > button:hover::after {
        animation: ripple 1s ease-out;
    }
    
    @keyframes ripple {
        0% {
            transform: scale(0, 0);
            opacity: 0.5;
        }
        100% {
            transform: scale(20, 20);
            opacity: 0;
        }
    }

    /* Enhanced sidebar styling */
    div[data-testid="stSidebar"] {
        background: linear-gradient(135deg, var(--card-bg-color) 0%, color-mix(in srgb, var(--card-bg-color) 85%, var(--primary-color) 15%) 100%);
        box-shadow: 2px 0 10px rgba(0, 0, 0, 0.2);
        animation: slideInLeft 0.5s ease-in-out;
    }
    
    div[data-testid="stSidebar"] > div:first-child {
        animation: slideInLeft 0.5s ease-in-out;
    }
    
    /* Sidebar title animation */
    div[data-testid="stSidebar"] h1 {
        position: relative;
        display: inline-block;
        background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
        background-size: 200% auto;
        background-clip: text;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: textGradient 3s linear infinite;
    }
    
    @keyframes textGradient {
        0% { background-position: 0% 50%; }
        100% { background-position: 200% 50%; }
    }
    
    /* Sidebar separator */
    div[data-testid="stSidebar"] hr {
        border: 0;
        height: 2px;
        background-image: linear-gradient(to right, transparent, var(--primary-color), transparent);
        margin: 15px 0;
        animation: glow 2s infinite alternate;
    }
    
    @keyframes glow {
        from { opacity: 0.7; }
        to { opacity: 1; }
    }

    /* Animated sidebar elements with staggered animation */
    div[data-testid="stSidebar"] > div:first-child > div > div > div {
        transform: translateX(-10px);
        opacity: 0;
        animation: slideInRight 0.5s forwards;
    }
    
    div[data-testid="stSidebar"] > div:first-child > div > div > div:nth-child(1) { animation-delay: 0.1s; }
    div[data-testid="stSidebar"] > div:first-child > div > div > div:nth-child(2) { animation-delay: 0.2s; }
    div[data-testid="stSidebar"] > div:first-child > div > div > div:nth-child(3) { animation-delay: 0.3s; }
    div[data-testid="stSidebar"] > div:first-child > div > div > div:nth-child(4) { animation-delay: 0.4s; }
    div[data-testid="stSidebar"] > div:first-child > div > div > div:nth-child(5) { animation-delay: 0.5s; }
    div[data-testid="stSidebar"] > div:first-child > div > div > div:nth-child(6) { animation-delay: 0.6s; }
    
    /* File uploader animation */
    div[data-testid="stFileUploader"] {
        border: 2px dashed var(--primary-color);
        border-radius: 8px;
        padding: 10px;
        transition: all 0.3s ease;
        animation: pulse 2s infinite alternate;
        background-color: color-mix(in srgb, var(--card-bg-color) 95%, var(--primary-color) 5%);
    }
    
    div[data-testid="stFileUploader"]:hover {
        border-color: var(--secondary-color);
        box-shadow: 0 0 10px rgba(76, 175, 80, 0.3);
        transform: scale(1.02);
    }
    
    /* Welcome container animations for front page */
    .welcome-container {
        animation: fadeIn 1s ease-in-out;
        margin-bottom: 2rem;
    }
    
    .welcome-title {
        animation: fadeInDown 0.8s ease-in-out;
    }
    
    .welcome-intro {
        animation: fadeIn 1s ease-in-out 0.3s;
        animation-fill-mode: both;
        line-height: 1.6;
    }
    
    .section-header {
        animation: fadeInDown 0.8s ease-in-out;
    }
    
    .step-card {
        background-color: color-mix(in srgb, var(--card-bg-color) 70%, black 30%);
        border-radius: 0.5rem;
        padding: 1rem;
        margin-bottom: 1rem;
        animation: slideInRight 0.5s ease-in-out calc(var(--animation-order) * 0.1s);
        animation-fill-mode: both;
        border-left: 3px solid var(--primary-color);
        transition: all 0.3s ease;
    }
    
    .step-card:hover {
        transform: translateX(5px);
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
        border-left-width: 5px;
    }
    
    .step-title {
        margin-top: 0;
    }
    
    .step-list li, .feature-list li {
        margin-bottom: 0.5rem;
        animation: fadeIn 0.5s ease-in-out calc((var(--li-order) * 0.1s) + 0.2s);
        animation-fill-mode: both;
    }
    
    .feature-name {
        font-weight: bold;
        color: var(--primary-color);
    }
    
    /* Interactive hover effects for lists */
    .step-list li:hover, .feature-list li:hover {
        transform: translateX(3px);
        color: var(--primary-color);
        transition: all 0.2s ease;
    }
    </style>
    """, unsafe_allow_html=True)

st.sidebar.title("WhatsApp Chat Analyzer")
st.sidebar.markdown("<hr>", unsafe_allow_html=True)

# Theme selector in sidebar with improved styling
st.sidebar.markdown("### 🎨 App Theme")
theme_options = {
    'dark_green': '🌲 Forest Green', 
    'midnight_blue': '🌃 Midnight Blue', 
    'sunset_orange': '🌅 Sunset Orange', 
    'deep_purple': '💜 Deep Purple'
}
selected_theme = st.sidebar.selectbox(
    "Choose a color theme", 
    options=list(theme_options.keys()),
    format_func=lambda x: theme_options[x],
    index=list(theme_options.keys()).index(st.session_state.theme)
)

# Update theme if changed
if selected_theme != st.session_state.theme:
    st.session_state.theme = selected_theme
    st.rerun()

# Create a splash screen animation for first-time visitors
if 'first_load' in st.session_state and st.session_state.first_load:
    # Create a splash screen with animation
    splash_container = st.empty()
    splash_container.markdown(f"""
    <div style="position: fixed; top: 0; left: 0; right: 0; bottom: 0; display: flex; 
         flex-direction: column; align-items: center; justify-content: center; z-index: 999; 
         background-color: {current_theme['background']}; animation: fadeOut 1.5s ease-in-out forwards;">
        <div style="text-align: center; animation: scaleUp 1s ease-in-out;">
            <h1 style="font-size: 3rem; color: {current_theme['primary']}; margin-bottom: 1rem;">
                💬 WhatsApp Chat Analyzer
            </h1>
            <p style="font-size: 1.2rem; color: {current_theme['text']}; margin-bottom: 1rem;">
                Turn your conversations into insights
            </p>
            <div style="margin-top: 2rem; animation: pulse 1.5s infinite;">
                <div style="width: 50px; height: 50px; border: 5px solid {current_theme['primary']}; 
                     border-radius: 50%; border-top-color: transparent; 
                     animation: spin 1s linear infinite; margin: 0 auto;"></div>
            </div>
        </div>
    </div>
    
    <style>
    @keyframes fadeOut {{
        0% {{ opacity: 1; }}
        70% {{ opacity: 1; }}
        100% {{ opacity: 0; visibility: hidden; }}
    }}
    
    @keyframes scaleUp {{
        0% {{ transform: scale(0.8); opacity: 0; }}
        100% {{ transform: scale(1); opacity: 1; }}
    }}
    
    @keyframes pulse {{
        0% {{ transform: scale(1); }}
        50% {{ transform: scale(1.05); }}
        100% {{ transform: scale(1); }}
    }}
    
    @keyframes spin {{
        0% {{ transform: rotate(0deg); }}
        100% {{ transform: rotate(360deg); }}
    }}
    </style>
    """, unsafe_allow_html=True)
    
    # Wait for a shorter time then remove the splash screen
    time.sleep(1.5)
    splash_container.empty()
    
    # Set first_load to False so the splash screen doesn't show again
    st.session_state.first_load = False

# Create a button for Future Features
if st.sidebar.button("🚀 Future Features"):
    st.markdown("""
        # 🌟 Coming Soon: The Future of Chat Analysis!

        ## 🔗 Live WhatsApp Integration
        Soon you'll be able to analyze your chats in real-time! Say goodbye to manual exports - just connect 
        your WhatsApp once and watch the magic happen.

        ## 🎯 Smart Priority Detection
        We're developing an AI-powered system that ensures you never miss important messages again!

        ## ⚡ Supercharged Analytics
        Get ready for analytics features that will transform how you understand your conversations:
        * AI-powered message categorization
        * Real-time sentiment tracking
        * Smart notification system
        * Predictive scoring for important messages
    """)

# Create separate buttons for analysis and sentiment
analysis_type = st.sidebar.radio(
    "Choose Analysis Type",
    ["Chat Analysis", "Sentiment Analysis", "Topic Analysis", "Time Comparison"]
)

uploaded_file = st.sidebar.file_uploader("Choose a file")

# Display a short, friendly welcome message only if no file is uploaded
if uploaded_file is None:
    # Add an animated welcome container
    st.markdown("""
    <div class="welcome-container">
        <h1 class="welcome-title">👋 Welcome to WhatsApp Chat Analyzer!</h1>
        <p class="welcome-intro">Turn your WhatsApp conversations into colorful charts and insights. Just export your chat, upload it here, and discover who talks most, what everyone's talking about, and even the emotional tone of your messages.</p>
    </div>
    """, unsafe_allow_html=True)

    # Add information about the new feature with animations
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("""
    <h2 class="section-header">✨ NEW! Chat Comparison Over Time</h2>
    <p class="welcome-intro">Our new time comparison feature lets you see how conversations evolve over different periods. Perfect for tracking relationship development, identifying communication changes, and spotting long-term patterns!</p>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="step-card" style="--animation-order: 1;">
            <h3 class="step-title">How to use:</h3>
            <ol class="step-list">
                <li style="--li-order: 1;">Upload your chat file</li>
                <li style="--li-order: 2;">Select "Time Comparison" from the analysis options</li>
                <li style="--li-order: 3;">Choose two date ranges to compare</li>
                <li style="--li-order: 4;">See how conversations have changed!</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="step-card" style="--animation-order: 2;">
            <h3 class="step-title">What you'll discover:</h3>
            <ul class="feature-list">
                <li style="--li-order: 1;"><span class="feature-name">Message Trends</span> - See frequency changes</li>
                <li style="--li-order: 2;"><span class="feature-name">Topic Evolution</span> - Track conversation shifts</li>
                <li style="--li-order: 3;"><span class="feature-name">Emotional Changes</span> - Monitor sentiment shifts</li>
                <li style="--li-order: 4;"><span class="feature-name">Activity Patterns</span> - Discover timing changes</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Add quick start guide with animations
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("""
    <h2 class="section-header">📝 Quick Start Guide</h2>
    <p>Follow these simple steps to analyze your chat:</p>
    """, unsafe_allow_html=True)
    
    # Create a more visual quick start guide with numbered steps
    st.markdown("""
    <div class="step-card" style="--animation-order: 1;">
        <h3 class="step-title">1️⃣ Upload your chat file</h3>
        <p>Export your chat from WhatsApp and upload it using the sidebar menu</p>
    </div>
    <div class="step-card" style="--animation-order: 2;">
        <h3 class="step-title">2️⃣ Choose an analysis type</h3>
        <p>Select Chat Analysis, Sentiment Analysis, or Topic Analysis to explore different aspects</p>
    </div>
    <div class="step-card" style="--animation-order: 3;">
        <h3 class="step-title">3️⃣ Select a person</h3>
        <p>Choose 'Overall' to analyze everyone or select a specific contact</p>
    </div>
    <div class="step-card" style="--animation-order: 4;">
        <h3 class="step-title">4️⃣ View your insights</h3>
        <p>Click the analysis button and explore beautiful visualizations of your chat data</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Move existing code here - keep the existing logic for processing the uploaded file
if uploaded_file is not None:
    try:
        # Try different encodings
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
            
        df = preprocessor.preprocess(data)
        if df is None:
            st.error("Error processing the chat file. Please ensure it's a valid WhatsApp chat export.")
            st.stop()
            
        # fetch unique user list
        user_list = df['user'].unique().tolist()
        
        if 'group_notification' in user_list:
            user_list.remove('group_notification')
        
        user_list.sort()
        user_list.insert(0, 'Overall')
        
        selected_user = st.sidebar.selectbox('Show Analysis wrt', user_list)
        
        if analysis_type == "Chat Analysis":
            # Enhanced button with animation
            chat_analysis_btn = st.sidebar.button('Show Chat Analysis')
            if chat_analysis_btn:
                # Add animated loading experience with more professional visuals
                with st.spinner('✨ Creating your chat analysis dashboard...'):
                    # Use a cleaner progress experience
                    progress_container = st.empty()
                    progress_container.markdown("""
                    <div style="display: flex; align-items: center; gap: 15px; margin: 20px 0; padding: 15px; border-radius: 5px; background-color: var(--card-bg-color); box-shadow: 0 4px 10px rgba(0,0,0,0.1);">
                        <div style="width: 30px; height: 30px; border: 3px solid var(--primary-color); border-radius: 50%; border-top-color: transparent; animation: spin 1s linear infinite;"></div>
                        <div>
                            <div style="font-weight: bold; color: var(--primary-color);">Processing your chat data</div>
                            <div style="font-size: 0.8rem; opacity: 0.7;">This will only take a moment...</div>
                        </div>
                    </div>
                    <style>
                        @keyframes spin {
                            0% { transform: rotate(0deg); }
                            100% { transform: rotate(360deg); }
                        }
                    </style>
                    """, unsafe_allow_html=True)
                    
                    # Get basic stats
                    num_msgs, num_words, num_of_media, links_length, links, filtered_df = helper.fetch_stats(selected_user, df)
                    # Wait a moment for better UX
                    time.sleep(0.5)
                    progress_container.empty()  # Remove progress bar when done
                
                # Header with user info
                st.markdown('<div class="section-card">', unsafe_allow_html=True)
                if selected_user != 'Overall':
                    st.markdown(f"""
                    <h1>Chat Analysis: <span style="color: var(--secondary-color);">{selected_user}</span></h1>
                    <p style="font-size: 1.1rem; opacity: 0.8;">Detailed analysis of messages and patterns for this contact.</p>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <h1>Chat Analysis: Overall Group</h1>
                    <p style="font-size: 1.1rem; opacity: 0.8;">Comprehensive analysis of all participants in this conversation.</p>
                    """, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Stats row with enhanced styling and animated metrics
                st.markdown('<div class="section-card">', unsafe_allow_html=True)
                st.subheader("📊 Key Metrics")
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Messages", f"{num_msgs:,}")
                with col2:
                    st.metric("Total Words", f"{num_words:,}")
                with col3:
                    st.metric("Media Shared", f"{num_of_media:,}")
                with col4:
                    st.metric("Links Shared", f"{links_length:,}")
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Chat data section
                st.markdown('<div class="section-card">', unsafe_allow_html=True)
                st.subheader("💬 Message Preview")
                st.dataframe(filtered_df, height=300, use_container_width=True)
                
                # Display links in an expandable section
                if links_length > 0:
                    with st.expander("🔗 View Shared Links"):
                        for link in links:
                            st.markdown(f"- [{link}]({link})")
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Most active users section
                if selected_user == 'Overall':
                    st.markdown('<div class="section-card">', unsafe_allow_html=True)
                    st.subheader("👥 Participant Activity")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        x, new_df = helper.busiest_persons(df)
                        fig, ax = plt.subplots(figsize=(10, 6))
                        bars = ax.bar(x.index, x.values)
                        plt.xticks(rotation=45, ha='right')
                        ax.set_facecolor('#1f2937')
                        fig.patch.set_facecolor('#1f2937')
                        ax.tick_params(colors='white')
                        ax.spines['bottom'].set_color('white')
                        ax.spines['top'].set_color('white')
                        ax.spines['left'].set_color('white')
                        ax.spines['right'].set_color('white')
                        
                        # Update bar colors to use our theme colors
                        for i, bar in enumerate(bars):
                            if i % 2 == 0:
                                bar.set_color('#673AB7')  # Deep Purple
                            else:
                                bar.set_color('#228B22')  # Forest Green
                        
                        ax.set_title('Message Count by User', color='white', fontsize=14)
                        ax.set_xlabel('User', color='white')
                        ax.set_ylabel('Number of Messages', color='white')
                        
                        st.pyplot(fig)
                    
                    with col2:
                        st.subheader("Participation Stats")
                        # Add percentage column for better context
                        st.dataframe(new_df, height=300, use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)

                # Word Cloud section
                st.markdown('<div class="section-card">', unsafe_allow_html=True)
                st.subheader("🔤 Word Cloud Visualization")
                st.markdown("""
                <p style="color: #8491A0; font-style: italic; margin-bottom: 1rem;">
                The size of each word represents how frequently it appears in your conversations.
                </p>
                """, unsafe_allow_html=True)
                
                df_wc = helper.create_word_cloud(selected_user, df)
                
                # Customize the wordcloud to use our theme colors
                if hasattr(df_wc, 'recolor'):
                    # Create a custom colormap with our theme colors
                    from matplotlib.colors import LinearSegmentedColormap
                    colors = ['#673AB7', '#9575CD', '#228B22', '#66BB6A']
                    custom_cmap = LinearSegmentedColormap.from_list('Purple_Green', colors, N=20)
                    df_wc = df_wc.recolor(colormap=custom_cmap, random_state=42)
                
                fig, ax = plt.subplots(figsize=(20, 10), dpi=300)
                ax.imshow(df_wc, interpolation='bilinear')
                ax.axis("off")
                ax.set_frame_on(False)
                fig.patch.set_facecolor('#1f2937')
                
                st.pyplot(fig)
                st.markdown('</div>', unsafe_allow_html=True)

                # Most common words section
                st.markdown('<div class="section-card">', unsafe_allow_html=True)
                st.subheader("📝 Most Common Words")
                
                most_common_df = helper.most_common_words(selected_user, df)
                fig, ax = plt.subplots(figsize=(10, 6))
                bars = ax.barh(most_common_df['name'], most_common_df['msg'])
                
                # Style the chart
                ax.set_facecolor('#1f2937')
                fig.patch.set_facecolor('#1f2937')
                ax.tick_params(colors='white')
                plt.xticks(color='white')
                plt.yticks(color='white')
                
                # Add alternating colors from our theme
                for i, bar in enumerate(bars):
                    if i % 2 == 0:
                        bar.set_color('#673AB7')  # Deep Purple
                    else:
                        bar.set_color('#228B22')  # Forest Green
                
                ax.set_title('Most Frequently Used Words', color='white', fontsize=14)
                ax.set_xlabel('Frequency', color='white')
                
                st.pyplot(fig)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Emoji analysis
                st.markdown('<div class="section-card">', unsafe_allow_html=True)
                emoji_df = helper.emoji_analysis(selected_user, df)
                st.subheader("😀 Emoji Analysis")
                
                st.dataframe(emoji_df, height=400, use_container_width=True)
                
                # Create a pie chart of top 10 emojis
                if not emoji_df.empty:
                    top_10_emojis = emoji_df.head(10)
                    fig = px.pie(
                        top_10_emojis,
                        values='count',
                        names='emoji',
                        title='Top 10 Most Used Emojis',
                        hole=0.3,
                        color_discrete_sequence=['#673AB7', '#9575CD', '#B39DDB', '#D1C4E9', '#228B22', '#66BB6A', '#A5D6A7', '#C8E6C9', '#7B1FA2', '#4CAF50']
                    )
                    # Update layout for consistent styling
                    fig.update_layout(
                        paper_bgcolor='#1f2937',
                        plot_bgcolor='#1f2937',
                        font=dict(color='white'),
                    )
                    st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Monthly timeline
                st.markdown('<div class="section-card">', unsafe_allow_html=True)
                st.subheader("📅 Monthly Message Activity")

                timeline, timeline_df = helper.timeline(selected_user, df)

                # Create an interactive monthly timeline plot
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=timeline['time'],
                    y=timeline['message'],
                    name='Monthly Messages',
                    mode='lines+markers',
                    line=dict(color='#673AB7', width=2),
                    marker=dict(color='#673AB7', size=8)
                ))

                # Add the 3-month moving average line
                timeline['message_ma3'] = timeline['message'].rolling(window=3).mean()
                fig.add_trace(go.Scatter(
                    x=timeline['time'],
                    y=timeline['message_ma3'],
                    name='3-Month Average',
                    mode='lines',
                    line=dict(color='#228B22', width=2, dash='dash'),
                ))
                
                # Update layout
                fig.update_layout(
                    title='Message Volume by Month',
                    xaxis_title='Month',
                    yaxis_title='Number of Messages',
                    paper_bgcolor='#1f2937',
                    plot_bgcolor='#1f2937',
                    font=dict(color='white'),
                    legend=dict(
                        bgcolor='#1f2937',
                        font=dict(color='white')
                    )
                )

                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)

                # Daily timeline
                st.markdown('<div class="section-card">', unsafe_allow_html=True)
                st.subheader("📊 Daily Message Activity")

                daily_timeline_data, daily_fig = helper.daily_timeline(selected_user, df)
                
                # Update layout for consistent styling
                daily_fig.update_layout(
                    paper_bgcolor='#1f2937',
                    plot_bgcolor='#1f2937',
                    font=dict(color='white')
                )
                
                st.plotly_chart(daily_fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)

                # Daily activeness
                st.markdown('<div class="section-card">', unsafe_allow_html=True)
                st.subheader("📊 Daily Activity Distribution")
                
                daily_activeness = helper.daily_activeness(selected_user, df)
                st.dataframe(daily_activeness, height=300, use_container_width=True)
                
                # Create bar chart for daily activity
                fig = px.bar(
                    daily_activeness,
                    x='day_name',
                    y='count',
                    title='Daily Activity Pattern',
                    color_discrete_sequence=['#673AB7'],
                )
                
                # Update layout for consistent styling
                fig.update_layout(
                    paper_bgcolor='#1f2937',
                    plot_bgcolor='#1f2937',
                    font=dict(color='white')
                )
                
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)

                # Monthly activeness
                st.markdown('<div class="section-card">', unsafe_allow_html=True)
                st.subheader("📅 Monthly Activity Analysis")
                
                montly_activeness = helper.montly_activeness(selected_user, df)
                col1, col2 = st.columns(2)
                
                with col1:
                    st.dataframe(montly_activeness, height=300, use_container_width=True)
                
                with col2:
                    fig = px.bar(
                        montly_activeness,
                        x='count',
                        y='month',
                        orientation='h',
                        title='Monthly Message Distribution',
                        color_discrete_sequence=['#228B22'],
                    )
                    
                    # Update layout for consistent styling
                    fig.update_layout(
                        paper_bgcolor='#1f2937',
                        plot_bgcolor='#1f2937',
                        font=dict(color='white')
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)

                # Heat map section
                st.markdown('<div class="section-card">', unsafe_allow_html=True)
                st.subheader("🔥 Message Activity Patterns")

                # Get heatmap data and both figures
                heatmap_data, fig1, fig2 = helper.activity_heatmap(selected_user, df)
                
                # Update layout for consistent styling
                fig1.update_layout(
                    paper_bgcolor='#1f2937',
                    plot_bgcolor='#1f2937',
                    font=dict(color='white')
                )
                
                fig2.update_layout(
                    paper_bgcolor='#1f2937',
                    plot_bgcolor='#1f2937',
                    font=dict(color='white')
                )
                
                st.plotly_chart(fig1, use_container_width=True)
                st.plotly_chart(fig2, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)

                # Response Time Analysis section with enhanced styling
                st.markdown('<div class="section-card">', unsafe_allow_html=True)
                st.subheader("⏱️ Response Time Analysis")
                st.markdown("""
                <p style="color: #8491A0; font-style: italic; margin-bottom: 1rem;">
                This analysis shows how quickly messages are typically answered in the conversation.
                </p>
                """, unsafe_allow_html=True)
                
                # Calculate response times
                df_with_response = helper.calculate_response_times(df)
                response_stats = helper.analyze_response_patterns(df_with_response, selected_user)
                
                st.dataframe(response_stats, height=300, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)

        elif analysis_type == "Sentiment Analysis":
            # Enhanced button with animation
            sentiment_analysis_btn = st.sidebar.button('Show Sentiment Analysis')
            if sentiment_analysis_btn:
                # Add animated loading experience with more professional visuals
                with st.spinner('💡 Analyzing message sentiments...'):
                    # Use a cleaner progress experience
                    progress_container = st.empty()
                    progress_container.markdown("""
                    <div style="display: flex; align-items: center; gap: 15px; margin: 20px 0; padding: 15px; border-radius: 5px; background-color: var(--card-bg-color); box-shadow: 0 4px 10px rgba(0,0,0,0.1);">
                        <div style="width: 30px; height: 30px; border: 3px solid var(--secondary-color); border-radius: 50%; border-top-color: transparent; animation: spin 1s linear infinite;"></div>
                        <div>
                            <div style="font-weight: bold; color: var(--secondary-color);">Analyzing sentiment patterns</div>
                            <div style="font-size: 0.8rem; opacity: 0.7;">Discovering emotional trends in your conversations...</div>
                        </div>
                    </div>
                    <style>
                        @keyframes spin {
                            0% { transform: rotate(0deg); }
                            100% { transform: rotate(360deg); }
                        }
                    </style>
                    """, unsafe_allow_html=True)
                    
                    # Analyze sentiment
                    sentiment_df = sentiment.analyze_sentiment(df, selected_user)
                    sentiment_stats = sentiment.get_sentiment_stats(sentiment_df)
                    # Wait a moment for better UX
                    time.sleep(0.7)  
                    progress_container.empty()  # Remove progress indicator when done
                
                # Enhanced header and description
                st.markdown("""
                <h1>Sentiment Analysis Dashboard</h1>
                <div class="info-box">
                    <p>This analysis examines the emotional tone of messages in your conversations, categorizing them as positive, negative, or neutral based on the language used.</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Stats cards with improved styling and animation
                st.markdown('<div class="section-card">', unsafe_allow_html=True)
                st.subheader("🧠 Emotional Tone Breakdown")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown(f"""
                    <div class="counter-animation floating" style="animation-delay: 0s;">
                        <div data-testid="stMetricValue" class="interactive-element" style="font-size: 2rem !important; font-weight: bold; color: var(--primary-color);">{sentiment_stats.get('Positive', 0):.1f}%</div>
                        <div data-testid="stMetricLabel" style="font-size: 1rem !important;">😊 Positive Messages</div>
                    </div>
                    """, unsafe_allow_html=True)
                with col2:
                    st.markdown(f"""
                    <div class="counter-animation floating" style="animation-delay: 0.5s;">
                        <div data-testid="stMetricValue" class="interactive-element" style="font-size: 2rem !important; font-weight: bold; color: var(--accent-color);">{sentiment_stats.get('Negative', 0):.1f}%</div>
                        <div data-testid="stMetricLabel" style="font-size: 1rem !important;">😔 Negative Messages</div>
                    </div>
                    """, unsafe_allow_html=True)
                with col3:
                    st.markdown(f"""
                    <div class="counter-animation floating" style="animation-delay: 1s;">
                        <div data-testid="stMetricValue" class="interactive-element" style="font-size: 2rem !important; font-weight: bold; color: var(--secondary-color);">{sentiment_stats.get('Neutral', 0):.1f}%</div>
                        <div data-testid="stMetricLabel" style="font-size: 1rem !important;">😐 Neutral Messages</div>
                    </div>
                    """, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Plot sentiment distribution
                st.markdown('<div class="section-card">', unsafe_allow_html=True)
                st.subheader("📊 Sentiment Distribution")
                
                # Update plot styling for consistency
                sentiment_pie = sentiment.plot_sentiment_pie(sentiment_stats)
                sentiment_pie.update_layout(
                    paper_bgcolor='#1f2937',
                    plot_bgcolor='#1f2937',
                    font=dict(color='white')
                )
                
                st.plotly_chart(sentiment_pie, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Plot sentiment trend
                st.markdown('<div class="section-card">', unsafe_allow_html=True)
                st.subheader("📈 Sentiment Trend Over Time")
                st.markdown("""
                <p style="color: #8491A0; font-style: italic; margin-bottom: 1rem;">
                This chart shows how the emotional tone of conversations changes over time.
                </p>
                """, unsafe_allow_html=True)
                
                # Update plot styling for consistency
                sentiment_trend = sentiment.plot_sentiment_trend(sentiment_df)
                sentiment_trend.update_layout(
                    paper_bgcolor='#1f2937',
                    plot_bgcolor='#1f2937',
                    font=dict(color='white')
                )
                
                st.plotly_chart(sentiment_trend, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Word Clouds by sentiment
                st.markdown('<div class="section-card">', unsafe_allow_html=True)
                st.subheader("🔤 Sentiment Word Clouds")
                st.markdown("""
                <p style="color: #8491A0; font-style: italic; margin-bottom: 1rem;">
                Visualizing the most common words in positive and negative messages.
                </p>
                """, unsafe_allow_html=True)
                
                # Generate and display word clouds
                pos_wc, neg_wc = sentiment.generate_sentiment_wordclouds(sentiment_df)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("<h3 style='text-align: center; color: #4CAF50;'>Positive Messages</h3>", unsafe_allow_html=True)
                    if pos_wc:
                        fig, ax = plt.subplots(figsize=(10, 6))
                        ax.imshow(pos_wc)
                        ax.axis('off')
                        plt.tight_layout(pad=0)
                        fig.patch.set_facecolor('#1f2937')
                        st.pyplot(fig, use_container_width=True)
                    else:
                        st.info("No positive messages found")
                        
                with col2:
                    st.markdown("<h3 style='text-align: center; color: #E6855E;'>Negative Messages</h3>", unsafe_allow_html=True)
                    if neg_wc:
                        fig, ax = plt.subplots(figsize=(10, 6))
                        ax.imshow(neg_wc)
                        ax.axis('off')
                        plt.tight_layout(pad=0)
                        fig.patch.set_facecolor('#1f2937')
                        st.pyplot(fig, use_container_width=True)
                    else:
                        st.info("No negative messages found")
                st.markdown('</div>', unsafe_allow_html=True)

        elif analysis_type == "Topic Analysis":
            # Enhanced button with animation
            topic_analysis_btn = st.sidebar.button('Show Topic Analysis')
            if topic_analysis_btn:
                # Add animated loading experience with more professional visuals
                with st.spinner('🔍 Discovering conversation topics...'):
                    # Use a cleaner progress experience
                    progress_container = st.empty()
                    progress_container.markdown("""
                    <div style="display: flex; align-items: center; gap: 15px; margin: 20px 0; padding: 15px; border-radius: 5px; background-color: var(--card-bg-color); box-shadow: 0 4px 10px rgba(0,0,0,0.1);">
                        <div style="width: 30px; height: 30px; border: 3px solid var(--accent-color); border-radius: 50%; border-top-color: transparent; animation: spin 1s linear infinite;"></div>
                        <div>
                            <div style="font-weight: bold; color: var(--accent-color);">Extracting conversation topics</div>
                            <div style="font-size: 0.8rem; opacity: 0.7;">Analyzing patterns and themes in your messages...</div>
                        </div>
                    </div>
                    <style>
                        @keyframes spin {
                            0% { transform: rotate(0deg); }
                            100% { transform: rotate(360deg); }
                        }
                    </style>
                    """, unsafe_allow_html=True)
                    
                    # Extract topics
                    topics_df = topic_analysis.extract_topics(df, selected_user)
                    # Wait a moment for better UX
                    time.sleep(0.9)  
                    progress_container.empty()  # Remove progress indicator when done
                
                # Enhanced header and description
                st.markdown("""
                <h1>Topic Analysis Dashboard</h1>
                <div class="info-box">
                    <p>This analysis identifies the main conversation topics in your chat using natural language processing techniques to categorize messages into common themes.</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Topic visualization with improved styling
                st.markdown('<div class="section-card">', unsafe_allow_html=True)
                st.subheader("📊 Topic Distribution")
                st.markdown("""
                <p style="color: #8491A0; font-style: italic; margin-bottom: 1rem;">
                The chart below shows the main topics discussed in your conversations and their relative frequency.
                </p>
                """, unsafe_allow_html=True)
                
                # Create visualization
                fig = topic_analysis.create_topic_visualization(topics_df)
                
                if fig is not None:
                    # Update layout for consistent styling
                    fig.update_layout(
                        paper_bgcolor='#1f2937',
                        plot_bgcolor='#1f2937',
                        font=dict(color='white')
                    )
                    st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Display detailed topic information
                st.markdown('<div class="section-card">', unsafe_allow_html=True)
                st.subheader("📋 Detailed Topic Analysis")
                st.markdown("""
                <p style="color: #8491A0; font-style: italic; margin-bottom: 1rem;">
                Detailed breakdown of topics with their relative strength and key words.
                </p>
                """, unsafe_allow_html=True)
                
                # Apply styling to the dataframe
                st.dataframe(topics_df, height=400, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Add summary statistics
                st.markdown('<div class="section-card">', unsafe_allow_html=True)
                st.subheader("📌 Topic Summary")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    top_topic = topics_df.iloc[0]
                    st.metric("🔝 Most Common Topic", f"{top_topic['topic_name']} ({top_topic['strength_percent']:.1f}%)")
                
                with col2:
                    avg_strength = topics_df['strength_percent'].mean()
                    st.metric("📊 Average Topic Strength", f"{avg_strength:.1f}%")
                
                with col3:
                    active_topics = len(topics_df[topics_df['strength_percent'] > 0])
                    st.metric("📑 Active Topics", active_topics)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Topic insights section
                st.markdown('<div class="section-card">', unsafe_allow_html=True)
                st.subheader("💡 Topic Insights")
                
                # Calculate some insights
                top_three_topics = topics_df.head(3)['topic_name'].tolist()
                least_discussed = topics_df.tail(3)['topic_name'].tolist()
                
                st.markdown(f"""
                <div style="margin: 1rem 0;">
                    <p><strong>Top Conversation Themes:</strong> {', '.join(top_three_topics)}</p>
                    <p><strong>Least Discussed Topics:</strong> {', '.join(least_discussed)}</p>
                    <p><strong>Topic Diversity:</strong> {active_topics} active topics out of {len(topics_df)} analyzed</p>
                </div>
                
                <div style="margin-top: 1.5rem;">
                    <h4>How to Use These Insights:</h4>
                    <ul>
                        <li>Identify main areas of interest in your conversations</li>
                        <li>Discover patterns in communication topics over time</li>
                        <li>Find out which topics might need more attention</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

        elif analysis_type == "Time Comparison":
            # Completely rebuilt Time Comparison section with simplified approach
            st.markdown("""
            <div class="section-card">
                <h1 class="welcome-title">📊 Time Comparison</h1>
                <p class="welcome-intro">Compare conversations across different time periods to discover how communication patterns have evolved.</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Make sure we have date information
            if 'only_date' not in df.columns:
                st.error("Date information is required for time comparison. Please make sure your chat export includes dates.")
                st.stop()
            
            # Simple date handling with direct conversion to Python dates
            all_dates = pd.to_datetime(df['only_date'])
            min_date = all_dates.min().date()
            max_date = all_dates.max().date()
            
            # Display date selection with enhanced styling
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.markdown("""
            <h2 class="section-header">📆 Select Time Periods to Compare</h2>
            <p style="color: #8491A0; font-style: italic; margin-bottom: 1rem;">
                Choose two different time periods to compare how conversation patterns have changed.
            </p>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown('<div class="step-card" style="--animation-order: 1;">', unsafe_allow_html=True)
                st.markdown("<h3 style='color: var(--secondary-color);'>Period 1</h3>", unsafe_allow_html=True)
                p1_start = st.date_input("Start date", min_date, key="p1_start")
                p1_end = st.date_input("End date", min_date + pd.Timedelta(days=30), key="p1_end")
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="step-card" style="--animation-order: 2;">', unsafe_allow_html=True)
                st.markdown("<h3 style='color: var(--accent-color);'>Period 2</h3>", unsafe_allow_html=True)
                p2_start = st.date_input("Start date", max_date - pd.Timedelta(days=30), key="p2_start")
                p2_end = st.date_input("End date", max_date, key="p2_end")
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Validate dates selection
            if p1_start >= p1_end:
                st.error("For Period 1, the start date must be before the end date.")
                st.stop()
            
            if p2_start >= p2_end:
                st.error("For Period 2, the start date must be before the end date.")
                st.stop()
                
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Add a visually enhanced button
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.markdown("""
            <h2 class="section-header">🔍 Generate Time Comparison</h2>
            <p style="color: #8491A0; font-style: italic; margin-bottom: 1rem;">
                Click below to analyze and compare the selected time periods.
            </p>
            """, unsafe_allow_html=True)
            
            # Add a simple button with no state management
            compare_button = st.button("✨ Compare Periods", key="simple_compare")
            st.markdown('</div>', unsafe_allow_html=True)
            
            # When button is clicked, perform a simplified analysis
            if compare_button:
                # Add a styled progress bar with enhanced visual feedback
                st.markdown('<div class="section-card">', unsafe_allow_html=True)
                st.markdown("<h3 style='text-align: center;'>Analyzing Conversations...</h3>", unsafe_allow_html=True)
                progress = st.progress(0)
                status_text = st.empty()
                
                try:
                    # Step 1: Filter data for both periods (10%)
                    status_text.markdown("<p style='color: var(--accent-color); text-align: center;'>Reading data for selected time periods...</p>", unsafe_allow_html=True)
                    progress.progress(10)
                    df['date_obj'] = pd.to_datetime(df['only_date']).dt.date
                    
                    df1 = df[df['date_obj'].between(p1_start, p1_end)]
                    df2 = df[df['date_obj'].between(p2_start, p2_end)]
                    
                    # Step 2: Check if we have data (20%)
                    status_text.markdown("<p style='color: var(--accent-color); text-align: center;'>Validating data...</p>", unsafe_allow_html=True)
                    progress.progress(20)
                    if len(df1) == 0 or len(df2) == 0:
                        st.warning("One or both periods contain no messages. Please select different date ranges.")
                        progress.empty()
                        status_text.empty()
                        st.markdown('</div>', unsafe_allow_html=True)
                        st.stop()
                    
                    # Step 3: Filter by selected user if needed (30%)
                    status_text.markdown("<p style='color: var(--accent-color); text-align: center;'>Filtering by selected user...</p>", unsafe_allow_html=True)
                    progress.progress(30)
                    if selected_user != 'Overall':
                        df1 = df1[df1['user'] == selected_user]
                        df2 = df2[df2['user'] == selected_user]
                    
                    # Step 4: Prepare basic statistics (40%)
                    status_text.markdown("<p style='color: var(--accent-color); text-align: center;'>Calculating message metrics...</p>", unsafe_allow_html=True)
                    progress.progress(40)
                    period1_count = len(df1)
                    period2_count = len(df2)
                    
                    days1 = (p1_end - p1_start).days + 1
                    days2 = (p2_end - p2_start).days + 1
                    
                    msgs_per_day1 = period1_count / max(days1, 1)
                    msgs_per_day2 = period2_count / max(days2, 1)
                    
                    # Step 5: Prepare simple visualizations (50%)
                    status_text.markdown("<p style='color: var(--accent-color); text-align: center;'>Preparing visualizations...</p>", unsafe_allow_html=True)
                    progress.progress(50)
                    
                    # Create comparison data
                    comparison_data = pd.DataFrame({
                        'Period': ['Period 1', 'Period 2'],
                        'Messages': [period1_count, period2_count],
                        'Messages per Day': [msgs_per_day1, msgs_per_day2]
                    })
                    
                    # Step 6: Display results (60%)
                    status_text.markdown("<p style='color: var(--accent-color); text-align: center;'>Generating comparison results...</p>", unsafe_allow_html=True)
                    progress.progress(60)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Header for the results section
                    st.markdown('<div class="section-card">', unsafe_allow_html=True)
                    st.markdown(f"""
                    <h2 class="section-header">📊 Comparison Results</h2>
                    <p style="color: #8491A0; font-style: italic; margin-bottom: 1rem;">
                        Comparing conversations from {p1_start.strftime('%b %d, %Y')} to {p1_end.strftime('%b %d, %Y')} vs. {p2_start.strftime('%b %d, %Y')} to {p2_end.strftime('%b %d, %Y')}
                    </p>
                    """, unsafe_allow_html=True)
                    
                    # Display metrics in a stylish layout
                    st.markdown("<h3 style='color: var(--secondary-color);'>Message Volume</h3>", unsafe_allow_html=True)
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Total Messages (Period 1)", period1_count)
                    with col2:
                        st.metric("Total Messages (Period 2)", period2_count)
                    with col3:
                        percent_change = ((period2_count - period1_count) / max(period1_count, 1)) * 100
                        st.metric("Change", f"{percent_change:.1f}%", delta=period2_count - period1_count)
                    
                    # Display daily metrics
                    st.markdown("<h3 style='color: var(--secondary-color);'>Daily Activity</h3>", unsafe_allow_html=True)
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Messages/Day (Period 1)", f"{msgs_per_day1:.1f}")
                    with col2:
                        st.metric("Messages/Day (Period 2)", f"{msgs_per_day2:.1f}")
                    with col3:
                        day_percent = ((msgs_per_day2 - msgs_per_day1) / max(msgs_per_day1, 1)) * 100
                        st.metric("Change/Day", f"{day_percent:.1f}%", delta=msgs_per_day2 - msgs_per_day1)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Step 7: Create professional visualizations (80%)
                    status_text.markdown("<p style='color: var(--accent-color); text-align: center;'>Creating interactive visualizations...</p>", unsafe_allow_html=True)
                    progress.progress(80)
                    
                    # Message count chart with professional styling
                    st.markdown('<div class="section-card">', unsafe_allow_html=True)
                    st.markdown("<h3 style='color: var(--secondary-color);'>Message Volume Comparison</h3>", unsafe_allow_html=True)
                    
                    # Use plotly for more professional charts
                    fig = go.Figure()
                    fig.add_trace(go.Bar(
                        x=['Period 1', 'Period 2'],
                        y=[period1_count, period2_count],
                        marker_color=[current_theme['secondary'], current_theme['accent']],
                        text=[period1_count, period2_count],
                        textposition='auto'
                    ))
                    
                    fig.update_layout(
                        title='Total Messages by Period',
                        xaxis_title='Time Period',
                        yaxis_title='Number of Messages',
                        paper_bgcolor='#1f2937',
                        plot_bgcolor='#1f2937',
                        font=dict(color='white'),
                        height=500
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Daily average chart with professional styling
                    st.markdown("<h3 style='color: var(--secondary-color);'>Daily Activity Comparison</h3>", unsafe_allow_html=True)
                    
                    fig = go.Figure()
                    fig.add_trace(go.Bar(
                        x=['Period 1', 'Period 2'],
                        y=[msgs_per_day1, msgs_per_day2],
                        marker_color=[current_theme['secondary'], current_theme['accent']],
                        text=[f"{msgs_per_day1:.1f}", f"{msgs_per_day2:.1f}"],
                        textposition='auto'
                    ))
                    
                    fig.update_layout(
                        title='Average Messages per Day',
                        xaxis_title='Time Period',
                        yaxis_title='Messages per Day',
                        paper_bgcolor='#1f2937',
                        plot_bgcolor='#1f2937',
                        font=dict(color='white'),
                        height=500
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Step 8: Add active user comparison (90%)
                    status_text.markdown("<p style='color: var(--accent-color); text-align: center;'>Analyzing user participation...</p>", unsafe_allow_html=True)
                    progress.progress(90)
                    
                    # User activity section
                    st.markdown('<div class="section-card">', unsafe_allow_html=True)
                    st.markdown("<h3 style='color: var(--secondary-color);'>User Activity Analysis</h3>", unsafe_allow_html=True)
                    
                    # Count users in each period
                    users1 = df1['user'].unique()
                    users2 = df2['user'].unique()
                    
                    # Create sets for easy comparison
                    users1_set = set(users1)
                    users2_set = set(users2)
                    
                    # Identify new and departing users
                    new_users = users2_set - users1_set
                    departing_users = users1_set - users2_set
                    common_users = users1_set.intersection(users2_set)
                    
                    # Display user stats with visual enhancements
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                        st.metric("Active Users (Period 1)", len(users1))
                        if len(users1) > 0:
                            most_active1 = df1['user'].value_counts().index[0] if len(df1['user'].value_counts()) > 0 else "None"
                            st.markdown(f"<p><strong>Most active:</strong> {most_active1}</p>", unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    with col2:
                        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                        st.metric("Active Users (Period 2)", len(users2))
                        if len(users2) > 0:
                            most_active2 = df2['user'].value_counts().index[0] if len(df2['user'].value_counts()) > 0 else "None"
                            st.markdown(f"<p><strong>Most active:</strong> {most_active2}</p>", unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Create a visual representation of user changes
                    st.markdown("<h4 style='color: var(--accent-color);'>User Participation Changes</h4>", unsafe_allow_html=True)
                    
                    # Create plot for user participation
                    if len(users1_set) > 0 or len(users2_set) > 0:
                        # Create a simple bar chart for user participation
                        user_fig = go.Figure()
                        
                        # Add bars for each category
                        categories = ['Only in Period 1', 'In Both Periods', 'Only in Period 2']
                        values = [len(users1_set - users2_set), len(common_users), len(users2_set - users1_set)]
                        
                        user_fig.add_trace(go.Bar(
                            x=categories,
                            y=values,
                            marker_color=[current_theme['secondary'], '#4CAF50', current_theme['accent']],
                            text=values,
                            textposition='auto'
                        ))
                        
                        user_fig.update_layout(
                            title='User Participation Changes',
                            xaxis_title='Participation Category',
                            yaxis_title='Number of Users',
                            paper_bgcolor='#1f2937',
                            plot_bgcolor='#1f2937',
                            font=dict(color='white'),
                            height=400
                        )
                        
                        st.plotly_chart(user_fig, use_container_width=True)
                    
                    # List new and departing users with styled components
                    if len(new_users) > 0:
                        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                        st.markdown("<h4 style='color: #4CAF50;'>New Participants in Period 2</h4>", unsafe_allow_html=True)
                        new_list = ', '.join(list(new_users)[:5]) + (f" and {len(new_users) - 5} more..." if len(new_users) > 5 else "")
                        st.markdown(f"<p>{new_list}</p>", unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    if len(departing_users) > 0:
                        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                        st.markdown("<h4 style='color: #E6855E;'>Participants from Period 1 not in Period 2</h4>", unsafe_allow_html=True)
                        departing_list = ', '.join(list(departing_users)[:5]) + (f" and {len(departing_users) - 5} more..." if len(departing_users) > 5 else "")
                        st.markdown(f"<p>{departing_list}</p>", unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Step 9: Add message pattern insights if enough data is available
                    if period1_count >= 10 and period2_count >= 10:
                        st.markdown('<div class="section-card">', unsafe_allow_html=True)
                        st.markdown("<h3 style='color: var(--secondary-color);'>Conversation Pattern Insights</h3>", unsafe_allow_html=True)
                        
                        insights_col1, insights_col2 = st.columns(2)
                        
                        # Activity by day of week
                        try:
                            # Add day of week analysis
                            df1['day_name'] = pd.to_datetime(df1['only_date']).dt.day_name()
                            df2['day_name'] = pd.to_datetime(df2['only_date']).dt.day_name()
                            
                            day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
                            
                            # Count messages by day
                            day_counts1 = df1['day_name'].value_counts().reindex(day_order).fillna(0)
                            day_counts2 = df2['day_name'].value_counts().reindex(day_order).fillna(0)
                            
                            # Calculate weeks for normalization
                            weeks1 = max(days1 / 7, 1)  # Prevent division by zero
                            weeks2 = max(days2 / 7, 1)
                            
                            # Normalize to messages per week
                            day_counts1_norm = day_counts1 / weeks1
                            day_counts2_norm = day_counts2 / weeks2
                            
                            with insights_col1:
                                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                                st.markdown("<h4 style='color: var(--accent-color);'>Activity by Day of Week</h4>", unsafe_allow_html=True)
                                
                                # Create day of week comparison chart
                                dow_fig = go.Figure()
                                
                                dow_fig.add_trace(go.Bar(
                                    x=day_order,
                                    y=day_counts1_norm,
                                    name='Period 1',
                                    marker_color=current_theme['secondary']
                                ))
                                
                                dow_fig.add_trace(go.Bar(
                                    x=day_order,
                                    y=day_counts2_norm,
                                    name='Period 2',
                                    marker_color=current_theme['accent']
                                ))
                                
                                dow_fig.update_layout(
                                    title='Messages by Day of Week (avg per week)',
                                    xaxis_title='Day of Week',
                                    yaxis_title='Average Messages',
                                    barmode='group',
                                    paper_bgcolor='#1f2937',
                                    plot_bgcolor='#1f2937',
                                    font=dict(color='white'),
                                    height=400
                                )
                                
                                st.plotly_chart(dow_fig, use_container_width=True)
                                st.markdown('</div>', unsafe_allow_html=True)
                            
                            # Identify most active day changes
                            most_active_day1 = day_counts1.idxmax() if not day_counts1.empty else "None"
                            most_active_day2 = day_counts2.idxmax() if not day_counts2.empty else "None"
                            
                            if most_active_day1 != most_active_day2:
                                st.info(f"The most active day changed from {most_active_day1} in Period 1 to {most_active_day2} in Period 2.")
                        except Exception as day_e:
                            st.warning(f"Could not analyze day of week patterns: {str(day_e)}")
                        
                        # Try to analyze hour patterns if hourly data is available
                        try:
                            with insights_col2:
                                if 'hour' in df1.columns or 'date' in df1.columns:
                                    # Generate hour column if needed
                                    if 'hour' not in df1.columns and 'date' in df1.columns:
                                        df1['hour'] = pd.to_datetime(df1['date']).dt.hour
                                    
                                    if 'hour' not in df2.columns and 'date' in df2.columns:
                                        df2['hour'] = pd.to_datetime(df2['date']).dt.hour
                                    
                                    if 'hour' in df1.columns and 'hour' in df2.columns:
                                        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                                        st.markdown("<h4 style='color: var(--accent-color);'>Activity by Hour of Day</h4>", unsafe_allow_html=True)
                                        
                                        # Prepare hourly data
                                        hour_data1 = df1['hour'].value_counts().sort_index()
                                        hour_data2 = df2['hour'].value_counts().sort_index()
                                        
                                        # Create hour indexes for all 24 hours
                                        all_hours = list(range(24))
                                        hour_data1 = hour_data1.reindex(all_hours).fillna(0)
                                        hour_data2 = hour_data2.reindex(all_hours).fillna(0)
                                        
                                        # Normalize by days
                                        hour_data1_norm = hour_data1 / max(days1, 1)
                                        hour_data2_norm = hour_data2 / max(days2, 1)
                                        
                                        # Create hour visualization
                                        hour_fig = go.Figure()
                                        
                                        hour_fig.add_trace(go.Scatter(
                                            x=all_hours,
                                            y=hour_data1_norm,
                                            mode='lines+markers',
                                            name='Period 1',
                                            line=dict(color=current_theme['secondary'], width=2),
                                            marker=dict(size=7)
                                        ))
                                        
                                        hour_fig.add_trace(go.Scatter(
                                            x=all_hours,
                                            y=hour_data2_norm,
                                            mode='lines+markers',
                                            name='Period 2',
                                            line=dict(color=current_theme['accent'], width=2),
                                            marker=dict(size=7)
                                        ))
                                        
                                        hour_fig.update_layout(
                                            title='Messages by Hour of Day (avg per day)',
                                            xaxis=dict(
                                                title='Hour of Day',
                                                tickmode='array',
                                                tickvals=all_hours,
                                                ticktext=[f"{h}:00" for h in all_hours]
                                            ),
                                            yaxis_title='Average Messages',
                                            paper_bgcolor='#1f2937',
                                            plot_bgcolor='#1f2937',
                                            font=dict(color='white'),
                                            height=400
                                        )
                                        
                                        st.plotly_chart(hour_fig, use_container_width=True)
                                        st.markdown('</div>', unsafe_allow_html=True)
                        except Exception as hour_e:
                            if 'hour' in df1.columns or 'date' in df1.columns:
                                st.warning(f"Could not analyze hourly patterns: {str(hour_e)}")
                        
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Step 10: Complete (100%)
                    status_text.markdown("<p style='color: var(--primary-color); text-align: center;'>Analysis complete!</p>", unsafe_allow_html=True)
                    progress.progress(100)
                    
                    # Final success card with insights summary
                    st.markdown('<div class="section-card">', unsafe_allow_html=True)
                    st.markdown("<h3 style='color: var(--primary-color); text-align: center;'>Comparison Summary</h3>", unsafe_allow_html=True)
                    
                    # Generate insights based on the data
                    insights = []
                    
                    if period2_count > period1_count:
                        insights.append(f"📈 Message volume increased by {percent_change:.1f}% from Period 1 to Period 2.")
                    elif period1_count > period2_count:
                        insights.append(f"📉 Message volume decreased by {abs(percent_change):.1f}% from Period 1 to Period 2.")
                    else:
                        insights.append("📊 Message volume remained the same between the two periods.")
                    
                    if msgs_per_day2 > msgs_per_day1:
                        insights.append(f"⚡ Daily activity increased from {msgs_per_day1:.1f} to {msgs_per_day2:.1f} messages per day.")
                    elif msgs_per_day1 > msgs_per_day2:
                        insights.append(f"🐢 Daily activity decreased from {msgs_per_day1:.1f} to {msgs_per_day2:.1f} messages per day.")
                    
                    if len(new_users) > 0:
                        insights.append(f"👋 {len(new_users)} new participants joined the conversation in Period 2.")
                    
                    if len(departing_users) > 0:
                        insights.append(f"👋 {len(departing_users)} participants from Period 1 were not active in Period 2.")
                    
                    # Display insights
                    for i, insight in enumerate(insights):
                        st.markdown(f"<p style='--li-order: {i+1};' class='step-list'>{insight}</p>", unsafe_allow_html=True)
                    
                    st.success("Time comparison analysis complete! Explore the visualizations above to understand how conversation patterns have evolved.")
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                except Exception as e:
                    # Clear progress elements on error
                    progress.empty()
                    status_text.empty()
                    
                    # Show friendly error with professional styling
                    st.markdown('<div class="section-card">', unsafe_allow_html=True)
                    st.error(f"An error occurred during analysis: {str(e)}")
                    st.info("Please try selecting different date ranges or check if your data contains the necessary information.")
                    st.markdown('</div>', unsafe_allow_html=True)

    except Exception as e:
        # Show error message and stop execution
        st.error(f"An error occurred: {str(e)}")
        st.stop()

# Add Plotly configuration for better interactivity
st.markdown("""
<script>
const config = {
    displayModeBar: true,
    responsive: true,
    scrollZoom: true,
    displaylogo: false,
    toImageButtonOptions: {
        format: 'png',
        filename: 'whatsapp_chart',
        height: 800,
        width: 1200
    },
    modeBarButtonsToAdd: ['zoom2d', 'pan2d', 'select2d', 'lasso2d', 'zoomIn2d', 'zoomOut2d', 'autoScale2d', 'resetScale2d']
};

document.addEventListener('DOMContentLoaded', function() {
    const plots = document.querySelectorAll('.js-plotly-plot');
    plots.forEach(plot => {
        plot.on('plotly_hover', function() {
            plot.style.transform = 'scale(1.01)';
            plot.style.transition = 'transform 0.2s ease';
        });
        plot.on('plotly_unhover', function() {
            plot.style.transform = 'scale(1)';
        });
    });
});
</script>
""", unsafe_allow_html=True)


