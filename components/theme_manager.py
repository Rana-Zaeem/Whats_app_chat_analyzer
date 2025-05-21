import streamlit as st

# =============================================
# THEME INITIALIZATION
# =============================================

def initialize_theme():
    """Initialize theme settings in session state if not already set"""
    if 'theme' not in st.session_state:
        # Default to light theme
        st.session_state.theme = 'dark'

def get_theme_options():
    """Return available theme options"""
    return {
        'light': '☀️ Light Mode',
        'dark': '🌙 Dark Mode',
    }

def toggle_theme():
    """Toggle between light and dark themes"""
    if st.session_state.theme == 'light':
        st.session_state.theme = 'dark'
    else:
        st.session_state.theme = 'light'

# =============================================
# THEME COLOR SCHEMES
# =============================================

def get_theme_colors():
    """Return color scheme based on current theme"""
    if st.session_state.theme == 'dark':
        return {
            'background': '#0E1117',
            'text': '#FAFAFA',
            'primary': '#4F8BF9',
            'secondary': '#606060',
            'accent': '#FF4B4B',
            'chart_colors': ['#4F8BF9', '#FF4B4B', '#36D399', '#F2C94C', '#9B51E0']
        }
    else:
        return {
            'background': '#FFFFFF',
            'text': '#31333F',
            'primary': '#2E86C1',
            'secondary': '#A0AEC0',
            'accent': '#FF4B4B',
            'chart_colors': ['#2E86C1', '#E74C3C', '#27AE60', '#F39C12', '#8E44AD']
        }

# =============================================
# CSS GENERATION AND APPLICATION
# =============================================

def apply_theme_css():
    """Apply CSS based on current theme"""
    theme_colors = get_theme_colors()
    
    # Build CSS with current theme colors
    theme_css = f"""
    <style>
        /* Theme variables */
        :root {{
            --background-color: {theme_colors['background']};
            --text-color: {theme_colors['text']};
            --primary-color: {theme_colors['primary']};
            --secondary-color: {theme_colors['secondary']};
            --accent-color: {theme_colors['accent']};
        }}
        
        /* Apply theme to Streamlit elements */
        .stApp {{
            background-color: var(--background-color);
            color: var(--text-color);
        }}
        
        .stTextInput > div > div > input {{
            color: var(--text-color);
        }}
        
        .stSelectbox, .stMultiselect {{
            color: var(--text-color);
        }}
        
        /* Custom styling for headers */
        h1, h2, h3 {{
            color: var(--primary-color);
        }}
        
        /* Custom styling for buttons */
        .stButton > button {{
            background-color: var(--primary-color);
            color: white;
            border: none;
            border-radius: 4px;
            padding: 0.5rem 1rem;
            transition: background-color 0.3s ease;
        }}
        
        .stButton > button:hover {{
            background-color: var(--accent-color);
        }}
    </style>
    """
    
    # Apply the CSS
    st.markdown(theme_css, unsafe_allow_html=True)