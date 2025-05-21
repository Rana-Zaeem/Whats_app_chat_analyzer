import streamlit as st
from components.theme_manager import get_theme_options

def setup_sidebar():
    """Set up the sidebar with all controls and options, including AI Summary radio option"""
    st.sidebar.title("WhatsApp Chat Analyzer")
    st.sidebar.markdown("<hr>", unsafe_allow_html=True)
    
    # Theme selector in sidebar with improved styling
    st.sidebar.markdown("### 🎨 App Theme")
    theme_options = get_theme_options()
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
    
    # Create a button for Future Features
    show_future = st.sidebar.button("🚀 Future Features")
    
    # Unified radio for all analysis types, including AI Summary
    analysis_type = st.sidebar.radio(
        "Choose Analysis Type",
        ["Chat Analysis", "Sentiment Analysis", "Topic Analysis", "Time Comparison"]
    )
    
    # File uploader
    uploaded_file = st.sidebar.file_uploader("Choose a file")
    
    # Return all values needed from sidebar
    return {
        'show_future': show_future,
        'analysis_type': analysis_type,
        'uploaded_file': uploaded_file
    }