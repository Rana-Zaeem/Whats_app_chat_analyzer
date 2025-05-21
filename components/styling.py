import streamlit as st

def apply_custom_css():
    """Apply custom CSS styling for the application"""
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

def apply_plotly_config():
    """Apply Plotly configuration for better interactivity"""
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