import streamlit as st
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import time
from matplotlib.colors import LinearSegmentedColormap

def run_chat_analysis(selected_user, df, helper):
    """Handle chat analysis visualization and UI"""
    chat_analysis_btn = st.sidebar.button('Chat Analysis')
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