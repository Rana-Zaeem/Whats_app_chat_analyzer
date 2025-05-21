# =============================================
# SECTION 1: IMPORTS
# =============================================
import streamlit as st
import plotly.graph_objects as go

# =============================================
# SECTION 2: RESPONSIVE STYLING FUNCTIONS
# =============================================

def apply_responsive_styles():
    """
    Apply responsive CSS styles to adapt the app for mobile and desktop
    
    This function injects CSS that makes the app respond to different 
    screen sizes and device types, improving usability across platforms.
    """
    st.markdown("""
    <style>
    /* Base responsive styles */
    .main .block-container {
        max-width: 100%;
        padding: 1rem;
    }
    
    /* Make all images responsive */
    img {
        max-width: 100%;
        height: auto;
    }
    
    /* Responsive text scaling */
    @media (max-width: 768px) {
        h1 {font-size: 1.8rem !important;}
        h2 {font-size: 1.5rem !important;}
        h3 {font-size: 1.3rem !important;}
        p, li {font-size: 0.9rem !important;}
        div[data-testid="stMetricValue"] {font-size: 1.5rem !important;}
    }
    
    /* Make tables and dataframes scrollable */
    div[data-testid="stTable"], div[data-testid="stDataFrame"] {
        width: 100%;
        overflow-x: auto;
    }
    
    /* Make Plotly charts responsive */
    .js-plotly-plot, .plotly, .plot-container {
        max-width: 100%;
        overflow-x: auto;
    }
    
    /* Fix column layout on mobile */
    @media (max-width: 768px) {
        div[data-testid="column"] {
            width: 100% !important;
            min-width: 100% !important;
            margin-bottom: 1rem;
        }
        
        /* Stack metrics on mobile */
        div[data-testid="metric-container"] {
            width: 50%;
            padding: 10px !important;
        }
        
        /* Reduce padding on cards */
        .section-card, .chart-container {
            padding: 0.8rem !important;
        }
        
        /* Adjust sidebar */
        section[data-testid="stSidebar"] {
            width: 100%;
            min-width: 100%;
        }
    }
    
    /* Tablet adjustments */
    @media (min-width: 769px) and (max-width: 1200px) {
        div[data-testid="stMetricValue"] {
            font-size: 1.8rem !important;
        }
    }
    
    /* Better buttons for touch devices */
    @media (hover: none) {
        button {
            min-height: 3rem;
        }
    }
    
    /* Make section cards responsive */
    .section-card {
        width: 100%;
        box-sizing: border-box;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Add JavaScript to handle resize events for plotly charts
    st.markdown("""
    <script>
    // Function to update Plotly charts on window resize
    function resizePlotlyCharts() {
        if (typeof Plotly !== 'undefined') {
            const plots = document.querySelectorAll('.js-plotly-plot');
            plots.forEach(plot => {
                Plotly.Plots.resize(plot);
            });
        }
    }
    
    // Add resize event listener
    window.addEventListener('resize', resizePlotlyCharts);
    </script>
    """, unsafe_allow_html=True)

# =============================================
# SECTION 3: CHART CONFIGURATION
# =============================================

def make_chart_responsive(fig):
    """
    Update a Plotly figure to be responsive
    
    Parameters:
    -----------
    fig : plotly.graph_objects.Figure
        A Plotly figure object
    
    Returns:
    --------
    plotly.graph_objects.Figure
        The updated figure with responsive settings
    """
    # Set responsive layout properties
    fig.update_layout(
        autosize=True,
        margin=dict(l=10, r=10, t=50, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    # Make font size responsive
    fig.update_layout(
        font=dict(size=14)
    )
    
    return fig

# =============================================
# SECTION 4: RESPONSIVE LAYOUT UTILITIES
# =============================================

def display_responsive_metrics(metrics_dict):
    """
    Display metrics in a responsive grid
    
    Parameters:
    -----------
    metrics_dict : dict
        Dictionary of {metric_name: value}
    """
    # For smaller screens, use 2 columns
    if is_mobile():
        cols = st.columns(2)
        for i, (name, value) in enumerate(metrics_dict.items()):
            with cols[i % 2]:
                st.metric(name, value)
    # For larger screens, use 4 columns
    else:
        cols = st.columns(min(4, len(metrics_dict)))
        for i, (name, value) in enumerate(metrics_dict.items()):
            with cols[i % len(cols)]:
                st.metric(name, value)

def is_mobile():
    """
    Attempt to detect if user is on a mobile device
    Based on viewport width stored in session state
    
    Returns:
    --------
    bool
        Boolean indicating if likely on mobile
    """
    # Get viewport width from session state if available
    viewport_width = st.session_state.get('viewport_width', 1200)
    return viewport_width < 768

def responsive_columns(num_desktop=2):
    """
    Create responsive columns that stack on mobile
    
    Parameters:
    -----------
    num_desktop : int
        Number of columns on desktop
    
    Returns:
    --------
    list
        List of column objects
    """
    if is_mobile():
        return [st.container()]  # Single column on mobile
    else:
        return st.columns(num_desktop)  # Multiple columns on desktop