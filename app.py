import streamlit as st
import preprocessor
from wordcloud import WordCloud
import helper
import sentiment
import topic_analysis
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

# Configure page settings and theme
st.set_page_config(
    page_title="WhatsApp Chat Analyzer",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS styling
st.markdown("""
    <style>
    /* Main container */
    .main {
        background-color: #0e1117;
        color: #fafafa;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #262730;
        padding: 2rem 1rem;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #fff;
        font-weight: 600;
        margin-bottom: 1rem;
    }

    /* Layout containers */
    .layout-container {
        display: flex;
        flex-wrap: wrap;
        gap: 1rem;
        margin: 1rem 0;
        align-items: flex-start;
        justify-content: space-between;
    }

    .chart-container {
        flex: 1 1 auto;
        min-width: 300px;
        background-color: #1f2937;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }

    .control-panel {
        flex: 0 0 auto;
        width: 250px;
        background-color: #1f2937;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-left: 1rem;
    }

    /* Ensure proper spacing between sections */
    .section-divider {
        margin: 2rem 0;
        border-top: 1px solid #374151;
    }

    /* Responsive adjustments */
    @media (max-width: 768px) {
        .layout-container {
            flex-direction: column;
        }
        .control-panel {
            width: 100%;
            margin-left: 0;
            margin-top: 1rem;
        }
    }
    
    /* Cards for metrics */
    div[data-testid="stMetricValue"] {
        background-color: #1f2937;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
        transition: transform 0.2s;
    }
    div[data-testid="stMetricValue"]:hover {
        transform: translateY(-2px);
    }
    
    /* DataFrames */
    .dataframe {
        background-color: #1f2937;
        border-radius: 0.5rem;
        border: 1px solid #374151;
    }
    
    /* Plotly charts */
    .js-plotly-plot {
        background-color: #1f2937;
        border-radius: 0.5rem;
        padding: 1rem;
    }
    
    /* Custom button styling */
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 0.3rem;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #45a049;
        transform: translateY(-1px);
    }
    
    /* File uploader */
    .stFileUploader {
        background-color: #1f2937;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 2px dashed #374151;
    }
    
    /* Select boxes */
    .stSelectbox {
        background-color: #1f2937;
        border-radius: 0.3rem;
    }

    .chat-analysis-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        gap: 2rem;
        padding: 1.5rem;
        flex-wrap: wrap;
        margin-bottom: 2rem;
    }

    .header-title {
        flex: 1;
        min-width: 200px;
    }

    .header-controls {
        flex: 0 0 auto;
        display: flex;
        gap: 1rem;
        align-items: center;
    }

    .chart-wrapper {
        background-color: #1f2937;
        border-radius: 0.5rem;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }

    /* Ensure proper spacing between elements */
    .stButton {
        margin: 0.5rem 0;
    }

    /* Responsive design adjustments */
    @media (max-width: 768px) {
        .chat-analysis-header {
            flex-direction: column;
            align-items: stretch;
        }
        
        .header-controls {
            width: 100%;
            justify-content: flex-start;
            margin-top: 1rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)

st.sidebar.title("Whatsapp Chat Analyzer")

# Create a button for Future Features
if st.sidebar.button("🚀 Future Features"):
    st.markdown("""
        # 🌟 Coming Soon: The Future of Chat Analysis!

        ## 🔗 Live WhatsApp Integration
        Soon you'll be able to analyze your chats in real-time! Say goodbye to manual exports - just connect 
        your WhatsApp once and watch the magic happen. See conversation patterns emerge as you chat, get 
        instant insights, and understand your communication style on the fly!

        ## 🎯 Smart Priority Detection
        We're developing an AI-powered system that ensures you never miss important messages again! Here's 
        what you'll get:
        * Color-coded highlights for crucial messages
        * Automatic importance scoring for each message
        * Custom filters to define what matters most to you

        ## ⚡ Supercharged Analytics
        Get ready for analytics features that will transform how you understand your conversations:
        * AI-powered message categorization to better organize your chats
        * Real-time sentiment tracking to understand emotional patterns
        * Smart notification system that knows when to alert you
        * Predictive scoring to identify important messages before you read them

        ---
        Stay tuned! These exciting features are being crafted with ❤️ just for you!
    """)

# Create separate buttons for analysis and sentiment
analysis_type = st.sidebar.radio(
    "Choose Analysis Type",
    ["Chat Analysis", "Sentiment Analysis", "Topic Analysis"]
)

uploaded_file = st.sidebar.file_uploader("Choose a file")
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

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.stop()

    if analysis_type == "Chat Analysis":
        if st.sidebar.button('Show Chat Analysis'):
            num_msgs, num_words, num_of_media, links_length, links, filtered_df = helper.fetch_stats(selected_user, df)
            
            st.markdown("""
                <div class="chat-analysis-header">
                    <div class="header-title">
                        <h2 style='color: #fff;'>Chat Analysis</h2>
                    </div>
                    <div class="header-controls">
                        <!-- Your control elements will be automatically wrapped here -->
                    </div>
                </div>
                
                <div class="chart-wrapper">
                    <!-- Your chart content -->
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
                <div class="layout-container">
                    <div class="chart-container">
                        <h3 style='color: #fff; margin-bottom: 1rem;'>Chat Messages</h3>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # Display the DataFrame according to the selected user
            st.dataframe(filtered_df, height=300)
            
            st.markdown("""<div class="section-divider"></div>""", unsafe_allow_html=True)
            
            st.markdown("""
                <div class="layout-container">
                    <div class="chart-container">
                        <h2 style='color: #fff; margin-bottom: 1.5rem;'>Chat Statistics</h2>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.markdown("""
                    <div style='background-color: #2563eb; color: white; padding: 1rem; border-radius: 0.5rem; text-align: center;'>
                        <h4 style='margin: 0;'>💬 Total Messages</h4>
                        <h2 style='margin: 0.5rem 0;'>{}</h2>
                    </div>
                """.format(num_msgs), unsafe_allow_html=True)
                
            with col2:
                st.markdown("""
                    <div style='background-color: #059669; color: white; padding: 1rem; border-radius: 0.5rem; text-align: center;'>
                        <h4 style='margin: 0;'>📝 Total Words</h4>
                        <h2 style='margin: 0.5rem 0;'>{}</h2>
                    </div>
                """.format(num_words), unsafe_allow_html=True)
                
            with col3:
                st.markdown("""
                    <div style='background-color: #7c3aed; color: white; padding: 1rem; border-radius: 0.5rem; text-align: center;'>
                        <h4 style='margin: 0;'>🖼️ Media Shared</h4>
                        <h2 style='margin: 0.5rem 0;'>{}</h2>
                    </div>
                """.format(num_of_media), unsafe_allow_html=True)
                
            with col4:
                st.markdown("""
                    <div style='background-color: #dc2626; color: white; padding: 1rem; border-radius: 0.5rem; text-align: center;'>
                        <h4 style='margin: 0;'>🔗 Links Shared</h4>
                        <h2 style='margin: 0.5rem 0;'>{}</h2>
                    </div>
                """.format(links_length), unsafe_allow_html=True)

            # Display links in an expandable section
            with st.expander("View Shared Links"):
                st.write(links)
                
            # Bussiest guy in group
            if selected_user == 'Overall':
                st.markdown("""
                    <div style='background-color: #1f2937; padding: 1.5rem; border-radius: 0.5rem; margin: 2rem 0;'>
                        <h2 style='color: #fff; margin-bottom: 1rem;'>Most Active Users</h2>
                    </div>
                """, unsafe_allow_html=True)
                
                x, new_df = helper.busiest_persons(df)
                col1, col2 = st.columns(2)
                with col1:
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
                    
                    # Add gradient colors to bars
                    for i, bar in enumerate(bars):
                        bar.set_color(plt.cm.viridis(i/len(bars)))
                    
                    st.pyplot(fig)
                
                with col2:
                    st.markdown("""
                        <div style='background-color: #1f2937; padding: 1rem; border-radius: 0.5rem;'>
                            <h4 style='color: #fff; margin-bottom: 1rem;'>Participation Stats</h4>
                        </div>
                    """, unsafe_allow_html=True)
                    st.dataframe(new_df, height=300)

            # Word Cloud section
            st.markdown("""
                <div style='background-color: #1f2937; padding: 2rem; border-radius: 0.8rem; margin: 2rem 0; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);'>
                    <h2 style='color: #fff; margin-bottom: 1.5rem; font-size: 1.8rem;'>Interactive Word Cloud Visualization</h2>
                    <p style='color: #9ca3af; margin-bottom: 1.5rem;'>Discover the most prominent words in your chat conversations</p>
                </div>
            """, unsafe_allow_html=True)
            
            df_wc = helper.create_word_cloud(selected_user, df)
            
            # Create figure with specific dimensions and high DPI for better quality
            fig, ax = plt.subplots(figsize=(20, 10), dpi=300)
            ax.imshow(df_wc, interpolation='bilinear')
            ax.axis("off")
            ax.set_frame_on(False)
            
            # Add padding around the word cloud
            plt.tight_layout(pad=3)
            
            # Set the figure background to match the app theme
            fig.patch.set_facecolor('#1f2937')
            
            # Create a container with custom styling
            with st.container():
                st.markdown("""
                    <style>
                        .word-cloud-container {
                            background-color: #1f2937;
                            border-radius: 0.8rem;
                            padding: 1rem;
                            margin: 1rem 0;
                            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
                        }
                    </style>
                    <div class="word-cloud-container">
                    </div>
                """, unsafe_allow_html=True)
                st.pyplot(fig)
                
            # Add interactive explanation
            with st.expander("ℹ️ About Word Cloud Visualization"):
                st.markdown("""
                    - **Size of Words**: Represents frequency in chat
                    - **Color Gradient**: Blue shades indicate different usage patterns
                    - **Word Placement**: Optimized for readability
                    - **Context**: Excludes common stop words and media messages
                """)

            # Most common words section
            st.markdown("""
                <div style='background-color: #1f2937; padding: 1.5rem; border-radius: 0.5rem; margin: 2rem 0;'>
                    <h2 style='color: #fff; margin-bottom: 1rem;'>Most Common Words</h2>
                </div>
            """, unsafe_allow_html=True)
            
            most_common_df = helper.most_common_words(selected_user, df)
            fig, ax = plt.subplots(figsize=(10, 6))
            bars = ax.barh(most_common_df['name'], most_common_df['msg'])
            
            # Style the chart
            ax.set_facecolor('#1f2937')
            fig.patch.set_facecolor('#1f2937')
            ax.tick_params(colors='white')
            plt.xticks(rotation='vertical', color='white')
            plt.yticks(color='white')
            
            # Add gradient colors to bars
            for i, bar in enumerate(bars):
                bar.set_color(plt.cm.cool(i/len(bars)))
            
            st.pyplot(fig)
            
            # emojis_analysis
            emoji_df = helper.emoji_analysis(selected_user,df)
            st.markdown("""
                <div style='background-color: #1f2937; padding: 1.5rem; border-radius: 0.5rem; margin: 2rem 0;'>
                    <h2 style='color: #fff; margin-bottom: 1rem;'>Emoji Analysis</h2>
                </div>
            """, unsafe_allow_html=True)
            
            # Display emoji dataset with improved formatting
            st.markdown("""
                <div style='background-color: #1f2937; padding: 1rem; border-radius: 0.5rem;'>
                    <h4 style='color: #fff; margin-bottom: 1rem;'>Emoji Usage Details</h4>
                </div>
            """, unsafe_allow_html=True)
            
            # Format the DataFrame for better display
            styled_df = emoji_df.style.set_properties(**{
                'background-color': '#1f2937',
                'color': 'white',
                'border-color': '#374151'
            })
            st.dataframe(styled_df, height=400)
            
            # Create a pie chart of top 10 emojis
            if not emoji_df.empty:
                top_10_emojis = emoji_df.head(10)
                fig = px.pie(
                    top_10_emojis,
                    values='count',
                    names='emoji',
                    title='Top 10 Most Used Emojis Distribution',
                    hole=0.3,  # Creates a donut chart effect
                )
                fig.update_layout(
                    showlegend=True,
                    paper_bgcolor='#1f2937',
                    plot_bgcolor='#1f2937',
                    font=dict(color='white'),
                    legend=dict(
                        bgcolor='#1f2937',
                        bordercolor='#374151'
                    ),
                    width=1000,  # Set a wider width
                    height=600,  # Set a taller height
                    margin=dict(t=50, b=50, l=50, r=50)  # Adjust margins for better spacing
                )
                fig.update_traces(
                    textposition='inside',
                    textinfo='percent+label'
                )
                # Use the full container width and configure the chart to be more prominent
                st.plotly_chart(fig, use_container_width=True, config={
                    'displayModeBar': True,
                    'displaylogo': False,
                    'scrollZoom': False,
                    'modeBarButtonsToRemove': ['zoom', 'pan', 'select', 'lasso2d']
                })
            
            # Monthly timeline
            st.markdown("""
                <div style='background-color: #1f2937; padding: 1.5rem; border-radius: 0.5rem; margin: 2rem 0;'>
                    <h2 style='color: #fff; margin-bottom: 1rem;'>Monthly Message Activity</h2>
                </div>
            """, unsafe_allow_html=True)

            timeline, timeline_df = helper.timeline(selected_user, df)

            # Create an interactive monthly timeline plot using Plotly
            fig = go.Figure()

            # Add the monthly message count line
            fig.add_trace(go.Scatter(
                x=timeline['time'],
                y=timeline['message'],
                name='Monthly Messages',
                mode='lines+markers',
                line=dict(color='#10b981', width=2),  # Emerald color
                marker=dict(
                    size=8,
                    symbol='circle',
                    line=dict(color='#fff', width=1)
                ),
                hovertemplate='Month: %{x}<br>Messages: %{y}<extra></extra>'
            ))

            # Add the 3-month moving average line
            timeline['message_ma3'] = timeline['message'].rolling(window=3).mean()
            fig.add_trace(go.Scatter(
                x=timeline['time'],
                y=timeline['message_ma3'],
                name='3-Month Average',
                mode='lines',
                line=dict(color='#f59e0b', width=2, dash='dash'),  # Amber color
                hovertemplate='Month: %{x}<br>3-Month Average: %{y:.1f}<extra></extra>'
            ))

            # Update the layout with improved styling
            fig.update_layout(
                template='plotly_dark',
                paper_bgcolor='#1f2937',
                plot_bgcolor='#1f2937',
                title=dict(
                    text='Message Volume by Month',
                    font=dict(size=20, color='white')
                ),
                xaxis=dict(
                    title='Month',
                    title_font=dict(size=16, color='white'),
                    tickfont=dict(size=12, color='white'),
                    gridcolor='#374151',
                    tickangle=45
                ),
                yaxis=dict(
                    title='Number of Messages',
                    title_font=dict(size=16, color='white'),
                    tickfont=dict(size=12, color='white'),
                    gridcolor='#374151'
                ),
                legend=dict(
                    bgcolor='#1f2937',
                    font=dict(color='white'),
                    bordercolor='#374151',
                    orientation='h',
                    yanchor='bottom',
                    y=1.02,
                    xanchor='right',
                    x=1
                ),
                hovermode='x unified',
                showlegend=True,
                width=1200,
                height=600,
                margin=dict(l=50, r=50, t=80, b=50)
            )

            # Show the interactive plot
            st.plotly_chart(fig, use_container_width=True, config={
                'displayModeBar': True,
                'displaylogo': False,
                'scrollZoom': True,
                'modeBarButtonsToAdd': ['zoom', 'pan', 'zoomIn', 'zoomOut', 'resetScale'],
                'responsive': True
            })

            # Add monthly statistics cards
            col1, col2, col3 = st.columns(3)
            
            with col1:
                peak_month = timeline.loc[timeline['message'].idxmax()]
                st.markdown(f"""
                    <div style='background-color: #10b981; color: white; padding: 1rem; border-radius: 0.5rem; text-align: center;'>
                        <h4 style='margin: 0;'>📈 Most Active Month</h4>
                        <h3 style='margin: 0.5rem 0;'>{peak_month['time']}</h3>
                        <p style='margin: 0;'>{peak_month['message']} messages</p>
                    </div>
                """, unsafe_allow_html=True)

            with col2:
                avg_monthly = timeline['message'].mean()
                st.markdown(f"""
                    <div style='background-color: #f59e0b; color: white; padding: 1rem; border-radius: 0.5rem; text-align: center;'>
                        <h4 style='margin: 0;'>📊 Average Monthly Messages</h4>
                        <h3 style='margin: 0.5rem 0;'>{avg_monthly:.1f}</h3>
                        <p style='margin: 0;'>messages per month</p>
                    </div>
                """, unsafe_allow_html=True)

            with col3:
                total_months = len(timeline)
                st.markdown(f"""
                    <div style='background-color: #6366f1; color: white; padding: 1rem; border-radius: 0.5rem; text-align: center;'>
                        <h4 style='margin: 0;'>📅 Total Active Months</h4>
                        <h3 style='margin: 0.5rem 0;'>{total_months}</h3>
                        <p style='margin: 0;'>months with activity</p>
                    </div>
                """, unsafe_allow_html=True)

            # Show the detailed monthly data in an expandable section
            with st.expander("View Detailed Monthly Data"):
                st.dataframe(timeline_df.style.background_gradient(cmap='Greens')
                           .set_properties(**{'background-color': '#1f2937',
                                           'color': 'white',
                                           'border-color': '#374151'}))

            # Daily timeline
            st.markdown("""
                <div style='background-color: #1f2937; padding: 1.5rem; border-radius: 0.5rem; margin: 2rem 0;'>
                    <h2 style='color: #fff; margin-bottom: 1rem; font-size: 2rem;'>Daily Message Activity</h2>
                    <p style='color: #9ca3af; margin-bottom: 1rem;'>Track message patterns across different days</p>
                </div>
            """, unsafe_allow_html=True)

            daily_timeline_data, daily_fig = helper.daily_timeline(selected_user, df)

            # Update the figure layout to be more prominent
            daily_fig.update_layout(
                height=600,  # Increased height
                margin=dict(l=50, r=50, t=50, b=50),
                paper_bgcolor='#1f2937',
                plot_bgcolor='#1f2937',
                title=dict(
                    font=dict(size=24, color='white', family='Arial Black'),
                    x=0.5,
                    xanchor='center'
                ),
                xaxis=dict(
                    title_font=dict(size=16, color='white'),
                    tickfont=dict(size=12, color='white'),
                    gridcolor='rgba(255, 255, 255, 0.1)',
                    linecolor='white'
                ),
                yaxis=dict(
                    title_font=dict(size=16, color='white'),
                    tickfont=dict(size=12, color='white'),
                    gridcolor='rgba(255, 255, 255, 0.1)',
                    linecolor='white'
                )
            )

            # Show the plot without container width to make it more prominent
            st.plotly_chart(daily_fig, use_container_width=False, config={
                'displayModeBar': True,
                'displaylogo': False,
                'scrollZoom': True,
                'modeBarButtonsToAdd': ['zoom', 'pan', 'zoomIn', 'zoomOut', 'resetScale'],
                'responsive': True
            })

            # Add statistics cards using the daily_timeline_data DataFrame
            col1, col2, col3 = st.columns(3)
            with col1:
                peak_day = daily_timeline_data.loc[daily_timeline_data['message'].idxmax()]
                st.markdown(f"""
                    <div style='background-color: #3b82f6; color: white; padding: 1rem; border-radius: 0.5rem; text-align: center;'>
                        <h4 style='margin: 0;'>📈 Peak Activity Day</h4>
                        <h3 style='margin: 0.5rem 0;'>{peak_day['only_date'].strftime('%B %d, %Y')}</h3>
                        <p style='margin: 0;'>{peak_day['message']} messages</p>
                    </div>
                """, unsafe_allow_html=True)

            with col2:
                avg_messages = daily_timeline_data['message'].mean()
                st.markdown(f"""
                    <div style='background-color: #059669; color: white; padding: 1rem; border-radius: 0.5rem; text-align: center;'>
                        <h4 style='margin: 0;'>📊 Average Daily Messages</h4>
                        <h3 style='margin: 0.5rem 0;'>{avg_messages:.1f}</h3>
                        <p style='margin: 0;'>messages per day</p>
                    </div>
                """, unsafe_allow_html=True)

            with col3:
                active_days = len(daily_timeline_data)
                st.markdown(f"""
                    <div style='background-color: #7c3aed; color: white; padding: 1rem; border-radius: 0.5rem; text-align: center;'>
                        <h4 style='margin: 0;'>📅 Active Days</h4>
                        <h3 style='margin: 0.5rem 0;'>{active_days}</h3>
                        <p style='margin: 0;'>days with messages</p>
                    </div>
                """, unsafe_allow_html=True)

            # daily activeness
            st.markdown("""
                <div style='background-color: #1f2937; padding: 1.5rem; border-radius: 0.5rem; margin: 2rem 0;'>
                    <h2 style='color: #fff; margin-bottom: 1rem;'>Daily Activity Distribution</h2>
                    <p style='color: #9ca3af; margin-bottom: 1rem;'>Analysis of message patterns across different days of the week</p>
                </div>
            """, unsafe_allow_html=True)
            
            daily_activeness = helper.daily_activeness(selected_user, df)
            
            # Create styled DataFrame display
            st.markdown("""
                <div style='background-color: #1f2937; padding: 1rem; border-radius: 0.5rem;'>
                    <h4 style='color: #fff; margin-bottom: 1rem;'>Daily Message Counts</h4>
                </div>
            """, unsafe_allow_html=True)
            
            # Style the DataFrame
            styled_df = daily_activeness.style.background_gradient(cmap='YlOrRd', subset=['count'])\
                .set_properties(**{
                    'background-color': '#1f2937',
                    'color': 'white',
                    'border-color': '#374151'
                })
            st.dataframe(styled_df, height=300)
            
            st.markdown("""
                <div style='background-color: #1f2937; padding: 1rem; border-radius: 0.5rem;'>
                    <h4 style='color: #fff; margin-bottom: 1rem;'>Daily Activity Pattern</h4>
                </div>
            """, unsafe_allow_html=True)
            
            # Create bar chart using Plotly with adjusted dimensions
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                x=daily_activeness['day_name'],
                y=daily_activeness['count'],
                marker_color='#10b981',  # Emerald color
                hovertemplate="<b>%{x}</b><br>" +
                            "Messages: %{y}<br>" +
                            "<extra></extra>"
            ))
            
            fig.update_layout(
                template='plotly_dark',
                paper_bgcolor='#1f2937',
                plot_bgcolor='#1f2937',
                margin=dict(t=30, b=50, l=50, r=50),  # Adjusted margins
                height=400,  # Fixed height
                xaxis=dict(
                    title='Day of Week',
                    title_font=dict(size=14, color='white'),
                    tickfont=dict(size=12, color='white'),
                    gridcolor='#374151',
                    tickangle=0  # Horizontal labels
                ),
                yaxis=dict(
                    title='Number of Messages',
                    title_font=dict(size=14, color='white'),
                    tickfont=dict(size=12, color='white'),
                    gridcolor='#374151'
                ),
                hoverlabel=dict(
                    bgcolor='#374151',
                    font_size=14,
                    font_family="Arial"
                ),
                autosize=True  # Allow the plot to be responsive
            )
            
            # Display the plot with use_container_width=True for better responsiveness
            st.plotly_chart(fig, use_container_width=True, config={
                'displayModeBar': True,
                'displaylogo': False,
                'modeBarButtonsToRemove': ['zoom', 'pan', 'select', 'lasso2d'],
                'responsive': True
            })
            
            # Add insights about daily patterns
            max_day = daily_activeness.loc[daily_activeness['count'].idxmax()]
            avg_messages = daily_activeness['count'].mean()
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"""
                    <div style='background-color: #10b981; color: white; padding: 1rem; border-radius: 0.5rem; text-align: center;'>
                        <h4 style='margin: 0;'>📅 Most Active Day</h4>
                        <h3 style='margin: 0.5rem 0;'>{max_day['day_name']}</h3>
                        <p style='margin: 0;'>{int(max_day['count'])} messages</p>
                    </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                    <div style='background-color: #3b82f6; color: white; padding: 1rem; border-radius: 0.5rem; text-align: center;'>
                        <h4 style='margin: 0;'>📊 Average Daily Messages</h4>
                        <h3 style='margin: 0.5rem 0;'>{avg_messages:.1f}</h3>
                        <p style='margin: 0;'>messages per day</p>
                    </div>
                """, unsafe_allow_html=True)
            
            with col3:
                activity_range = max_day['count'] - daily_activeness['count'].min()
                st.markdown(f"""
                    <div style='background-color: #8b5cf6; color: white; padding: 1rem; border-radius: 0.5rem; text-align: center;'>
                        <h4 style='margin: 0;'>📈 Activity Range</h4>
                        <h3 style='margin: 0.5rem 0;'>{int(activity_range)}</h3>
                        <p style='margin: 0;'>message variance</p>
                    </div>
                """, unsafe_allow_html=True)

            # mountly activeness
            st.markdown("""
                <div style='background-color: #1f2937; padding: 1.5rem; border-radius: 0.5rem; margin: 2rem 0;'>
                    <h2 style='color: #fff; margin-bottom: 1rem;'>Monthly Activity Analysis</h2>
                    <p style='color: #9ca3af; margin-bottom: 1rem;'>Distribution of messages across different months</p>
                </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)  
            montly_activeness = helper.montly_activeness(selected_user,df)
            
            with col1:
                # Style the DataFrame
                styled_df = montly_activeness.style.background_gradient(cmap='YlOrRd', subset=['count'])\
                    .set_properties(**{
                        'background-color': '#1f2937',
                        'color': 'white',
                        'border-color': '#374151'
                    })
                st.dataframe(styled_df, height=300)
            
            with col2:
                # Create interactive bar chart using Plotly
                fig = go.Figure()
                
                fig.add_trace(go.Bar(
                    x=montly_activeness['count'],
                    y=montly_activeness['month'],
                    orientation='h',
                    marker_color='#f59e0b',
                    hovertemplate="<b>%{y}</b><br>" +
                                "Messages: %{x}<br>" +
                                "<extra></extra>"
                ))
                
                fig.update_layout(
                    title=dict(
                        text='Monthly Message Distribution',
                        font=dict(size=16, color='white'),
                        x=0.5
                    ),
                    template='plotly_dark',
                    paper_bgcolor='#1f2937',
                    plot_bgcolor='#1f2937',
                    margin=dict(l=20, r=20, t=40, b=20),
                    xaxis=dict(
                        title='Number of Messages',
                        title_font=dict(size=14, color='white'),
                        tickfont=dict(size=12, color='white'),
                        gridcolor='#374151',
                        showgrid=True
                    ),
                    yaxis=dict(
                        title='',
                        tickfont=dict(size=12, color='white'),
                        gridcolor='#374151',
                        automargin=True  # This ensures labels don't get cut off
                    ),
                    hoverlabel=dict(
                        bgcolor='#374151',
                        font_size=14,
                        font_family="Arial"
                    ),
                    height=400  # Adjust height to accommodate all labels
                )
                
                st.plotly_chart(fig, use_container_width=True)

            # Heat map section
            st.markdown("""
                <div style='background-color: #1f2937; padding: 2rem; border-radius: 0.8rem; margin: 2rem 0; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);'>
                    <h2 style='color: #fff; margin-bottom: 1rem; font-size: 1.8rem;'>Message Activity Patterns</h2>
                    <p style='color: #9ca3af; margin-bottom: 1rem;'>Discover when your chat is most active throughout the week</p>
                </div>
            """, unsafe_allow_html=True)

            # Get heatmap data and both figures
            heatmap_data, fig1, fig2 = helper.activity_heatmap(selected_user, df)

            # Display first heatmap with a description
            st.markdown("""
                <div style='background-color: #1f2937; padding: 1.5rem; border-radius: 0.5rem; margin: 1rem 0;'>
                    <h3 style='color: #fff; margin-bottom: 0.5rem;'>Overview Pattern</h3>
                    <p style='color: #9ca3af;'>A clean visualization of message activity across different times and days</p>
                </div>
            """, unsafe_allow_html=True)

            # Container for the first heatmap with full width
            st.plotly_chart(fig1, use_container_width=True)

            # Display second heatmap with a description
            st.markdown("""
                <div style='background-color: #1f2937; padding: 1.5rem; border-radius: 0.5rem; margin: 2rem 0 1rem 0;'>
                    <h3 style='color: #fff; margin-bottom: 0.5rem;'>Detailed View</h3>
                    <p style='color: #9ca3af;'>Exact message counts for each time slot throughout the week</p>
                </div>
            """, unsafe_allow_html=True)

            # Container for the second heatmap with full width
            st.plotly_chart(fig2, use_container_width=True)

            # Response Time Analysis section
            st.markdown("""
                <div style='background-color: #1f2937; padding: 1.5rem; border-radius: 0.8rem; margin: 2rem 0;'>
                    <h2 style='color: #fff; margin-bottom: 1rem;'>Response Time Analysis</h2>
                    <p style='color: #9ca3af;'>Analyzing how quickly users respond to messages</p>
                </div>
            """, unsafe_allow_html=True)
            
            # Calculate response times
            df_with_response = helper.calculate_response_times(df)
            response_stats = helper.analyze_response_patterns(df_with_response, selected_user)
            
            # Display response time statistics
            st.markdown("""
                <div style='background-color: #1f2937; padding: 1rem; border-radius: 0.5rem; margin-bottom: 1rem;'>
                    <h3 style='color: #fff; text-align: center;'>Response Time Statistics</h3>
                </div>
            """, unsafe_allow_html=True)
            
            # Format and display the statistics
            styled_stats = response_stats.style.background_gradient(cmap='YlOrRd')\
                .set_properties(**{
                    'background-color': '#1f2937',
                    'color': 'white',
                    'border-color': '#374151'
                })
            st.dataframe(styled_stats, height=300)
            
            # Add summary cards
            col1, col2, col3 = st.columns(3)
            
            with col1:
                avg_response = response_stats['avg_response_time'].mean()
                st.markdown(f"""
                    <div style='background-color: #10b981; color: white; padding: 1rem; border-radius: 0.5rem; text-align: center;'>
                        <h4 style='margin: 0;'>⚡ Average Response Time</h4>
                        <h2 style='margin: 0.5rem 0;'>{avg_response:.1f} min</h2>
                    </div>
                """, unsafe_allow_html=True)
            
            with col2:
                fastest_response = response_stats['min_response_time'].min()
                st.markdown(f"""
                    <div style='background-color: #3b82f6; color: white; padding: 1rem; border-radius: 0.5rem; text-align: center;'>
                        <h4 style='margin: 0;'>⚡ Fastest Response</h4>
                        <h2 style='margin: 0.5rem 0;'>{fastest_response:.1f} min</h2>
                    </div>
                """, unsafe_allow_html=True)
            
            with col3:
                slowest_response = response_stats['max_response_time'].max()
                st.markdown(f"""
                    <div style='background-color: #8b5cf6; color: white; padding: 1rem; border-radius: 0.5rem; text-align: center;'>
                        <h4 style='margin: 0;'>🐌 Slowest Response</h4>
                        <h2 style='margin: 0.5rem 0;'>{slowest_response:.1f} min</h2>
                    </div>
                """, unsafe_allow_html=True)

    elif analysis_type == "Sentiment Analysis":
        if st.sidebar.button('Show Sentiment Analysis'):
            # Title section with improved styling
            st.markdown("""
                <div style='background-color: #1f2937; padding: 2rem; border-radius: 0.8rem; margin: 2rem 0; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);'>
                    <h1 style='color: #fff; margin-bottom: 1rem;'>Sentiment Analysis Dashboard</h1>
                    <p style='color: #9ca3af;'>Analyzing the emotional tone of your chat messages</p>
                </div>
            """, unsafe_allow_html=True)
            
            # Analyze sentiment
            sentiment_df = sentiment.analyze_sentiment(df, selected_user)
            sentiment_stats = sentiment.get_sentiment_stats(sentiment_df)
            
            # Stats cards with improved visibility
            st.markdown("<div style='margin: 2rem 0;'>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f"""
                    <div style='background-color: #2563eb; color: white; padding: 1.5rem; border-radius: 0.8rem; text-align: center; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);'>
                        <h3 style='margin: 0; font-size: 1.2rem;'>😊 Positive Messages</h3>
                        <h2 style='margin: 1rem 0; font-size: 2rem;'>{sentiment_stats.get('Positive', 0):.1f}%</h2>
                    </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                    <div style='background-color: #dc2626; color: white; padding: 1.5rem; border-radius: 0.8rem; text-align: center; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);'>
                        <h3 style='margin: 0; font-size: 1.2rem;'>😔 Negative Messages</h3>
                        <h2 style='margin: 1rem 0; font-size: 2rem;'>{sentiment_stats.get('Negative', 0):.1f}%</h2>
                    </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                    <div style='background-color: #9ca3af; color: white; padding: 1.5rem; border-radius: 0.8rem; text-align: center; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);'>
                        <h3 style='margin: 0; font-size: 1.2rem;'>😐 Neutral Messages</h3>
                        <h2 style='margin: 1rem 0; font-size: 2rem;'>{sentiment_stats.get('Neutral', 0):.1f}%</h2>
                    </div>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Sentiment Distribution section
            st.markdown("""
                <div style='background-color: #1f2937; padding: 1.5rem; border-radius: 0.8rem; margin: 2rem 0;'>
                    <h2 style='color: #fff; margin-bottom: 1rem;'>Sentiment Distribution</h2>
                    <p style='color: #9ca3af;'>Distribution of message sentiments across the conversation</p>
                </div>
            """, unsafe_allow_html=True)
            
            # Plot sentiment distribution
            st.plotly_chart(sentiment.plot_sentiment_pie(sentiment_stats), use_container_width=True)
            
            # Sentiment Trend section
            st.markdown("""
                <div style='background-color: #1f2937; padding: 1.5rem; border-radius: 0.8rem; margin: 2rem 0;'>
                    <h2 style='color: #fff; margin-bottom: 1rem;'>Sentiment Trend Over Time</h2>
                    <p style='color: #9ca3af;'>How message sentiment changes over the course of conversations</p>
                </div>
            """, unsafe_allow_html=True)
            
            # Plot sentiment trend
            st.plotly_chart(sentiment.plot_sentiment_trend(sentiment_df), use_container_width=True)
            
            # Word Clouds section
            st.markdown("""
                <div style='background-color: #1f2937; padding: 1.5rem; border-radius: 0.8rem; margin: 2rem 0;'>
                    <h2 style='color: #fff; margin-bottom: 1rem;'>Word Clouds by Sentiment</h2>
                    <p style='color: #9ca3af;'>Most frequent words in positive and negative messages</p>
                </div>
            """, unsafe_allow_html=True)
            
            # Generate and display word clouds
            pos_wc, neg_wc = sentiment.generate_sentiment_wordclouds(sentiment_df)
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("""
                    <div style='background-color: #1f2937; padding: 1rem; border-radius: 0.5rem; margin-bottom: 1rem;'>
                        <h3 style='color: #fff; text-align: center;'>Positive Messages</h3>
                    </div>
                """, unsafe_allow_html=True)
                if pos_wc:
                    fig, ax = plt.subplots(figsize=(10, 6))
                    ax.imshow(pos_wc)
                    ax.axis('off')
                    plt.tight_layout(pad=0)
                    st.pyplot(fig, use_container_width=True)
                else:
                    st.info("No positive messages found")
                    
            with col2:
                st.markdown("""
                    <div style='background-color: #1f2937; padding: 1rem; border-radius: 0.5rem; margin-bottom: 1rem;'>
                        <h3 style='color: #fff; text-align: center;'>Negative Messages</h3>
                    </div>
                """, unsafe_allow_html=True)
                if neg_wc:
                    fig, ax = plt.subplots(figsize=(10, 6))
                    ax.imshow(neg_wc)
                    ax.axis('off')
                    plt.tight_layout(pad=0)
                    st.pyplot(fig, use_container_width=True)
                else:
                    st.info("No negative messages found")

    else:  # Topic Analysis
        if st.sidebar.button('Show Topic Analysis'):
            # Title section
            st.markdown("""
                <div style='background-color: #1f2937; padding: 2rem; border-radius: 0.8rem; margin: 2rem 0; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);'>
                    <h1 style='color: #fff; margin-bottom: 1rem;'>Topic Analysis Dashboard</h1>
                    <p style='color: #9ca3af;'>Discover the main topics of discussion in your chat</p>
                </div>
            """, unsafe_allow_html=True)
            
            # Extract topics
            topics_df = topic_analysis.extract_topics(df, selected_user)
            
            # Create visualization
            fig = topic_analysis.create_topic_visualization(topics_df)
            
            if fig is not None:
                st.plotly_chart(fig, use_container_width=True)
            
            # Display detailed topic information
            st.markdown("""
                <div style='background-color: #1f2937; padding: 1.5rem; border-radius: 0.8rem; margin: 2rem 0;'>
                    <h2 style='color: #fff; margin-bottom: 1rem;'>Detailed Topic Analysis</h2>
                    <p style='color: #9ca3af;'>Breakdown of topics with their relative strengths and key words</p>
                </div>
            """, unsafe_allow_html=True)
            
            # Style the DataFrame display
            styled_df = topics_df.style.background_gradient(cmap='YlOrRd', subset=['strength_percent'])\
                .set_properties(**{
                    'background-color': '#1f2937',
                    'color': 'white',
                    'border-color': '#374151'
                })
            st.dataframe(styled_df, height=400)
            
            # Add summary statistics
            col1, col2, col3 = st.columns(3)
            
            with col1:
                top_topic = topics_df.iloc[0]
                st.markdown(f"""
                    <div style='background-color: #2563eb; color: white; padding: 1rem; border-radius: 0.5rem; text-align: center;'>
                        <h4 style='margin: 0;'>🔝 Most Common Topic</h4>
                        <h3 style='margin: 0.5rem 0;'>{top_topic['topic_name']}</h3>
                        <p style='margin: 0;'>{top_topic['strength_percent']:.1f}% of messages</p>
                    </div>
                """, unsafe_allow_html=True)
            
            with col2:
                avg_strength = topics_df['strength_percent'].mean()
                st.markdown(f"""
                    <div style='background-color: #059669; color: white; padding: 1rem; border-radius: 0.5rem; text-align: center;'>
                        <h4 style='margin: 0;'>📊 Average Topic Strength</h4>
                        <h3 style='margin: 0.5rem 0;'>{avg_strength:.1f}%</h3>
                        <p style='margin: 0;'>across all topics</p>
                    </div>
                """, unsafe_allow_html=True)
            
            with col3:
                active_topics = len(topics_df[topics_df['strength_percent'] > 0])
                st.markdown(f"""
                    <div style='background-color: #7c3aed; color: white; padding: 1rem; border-radius: 0.5rem; text-align: center;'>
                        <h4 style='margin: 0;'>📑 Active Topics</h4>
                        <h3 style='margin: 0.5rem 0;'>{active_topics}</h3>
                        <p style='margin: 0;'>topics detected</p>
                    </div>
                """, unsafe_allow_html=True)


