import streamlit as st
import time

def run_topic_analysis(selected_user, df, topic_analysis):
    """Handle topic analysis visualization and UI"""
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