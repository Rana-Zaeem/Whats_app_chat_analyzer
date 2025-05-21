import streamlit as st
import time
import matplotlib.pyplot as plt

def run_sentiment_analysis(selected_user, df, sentiment):
    """Handle sentiment analysis visualization and UI"""
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
        Visualizing the most common words in positive, negative, and neutral messages.
        </p>
        """, unsafe_allow_html=True)
        
        # Generate and display word clouds
        pos_wc, neg_wc, neu_wc = sentiment.generate_sentiment_wordclouds(sentiment_df)
        
        col1, col2, col3 = st.columns(3)
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
                
        with col3:
            st.markdown("<h3 style='text-align: center; color: #3F51B5;'>Neutral Messages</h3>", unsafe_allow_html=True)
            if neu_wc:
                fig, ax = plt.subplots(figsize=(10, 6))
                ax.imshow(neu_wc)
                ax.axis('off')
                plt.tight_layout(pad=0)
                fig.patch.set_facecolor('#1f2937')
                st.pyplot(fig, use_container_width=True)
            else:
                st.info("No neutral messages found")
        st.markdown('</div>', unsafe_allow_html=True)

        # =============================================
        # Sentiment & Toxicity Analysis (AI Powered, Modern Graphs)
        # =============================================
        from models import sentiment_toxicity
        import plotly.express as px
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("🧠 Sentiment & Toxicity Analysis (AI Powered)")
        st.markdown("""
        <div style="color: #8491A0; font-style: italic; margin-bottom: 1rem;">
        This section uses AI/NLP to analyze the <b>mood</b> (sentiment) and <b>toxicity</b> (offensive/abusive language) of your chat group or selected user.<br>
        <ul style='margin-top: 0.5rem;'>
            <li><b>Sentiment</b>: Measures if a message is <span style='color:#4CAF50;'>positive</span>, <span style='color:#E6855E;'>negative</span>, or <span style='color:#3F51B5;'>neutral</span> in tone.</li>
            <li><b>Toxicity</b>: Detects if a message contains <span style='color:#E53935;'>abusive, offensive, or rude words</span> (see info below).</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

        with st.expander("ℹ️ What do these terms mean? Click to learn more."):
            st.markdown("""
            - <b>Avg Sentiment</b>: Average mood score for each user. Positive = happy/supportive, Negative = angry/sad, Neutral = normal.
            - <b>Positive/Negative/Neutral Msgs</b>: Number of messages by sentiment type.
            - <b>Toxic Msgs</b>: Number of messages by a user that contain abusive or offensive words (e.g., 'stupid', 'idiot', 'gandu', etc.).
            - <b>Toxicity Ratio</b>: Fraction of a user's messages that are toxic (0 = clean, 1 = all toxic).
            - <b>Group Avg Sentiment</b>: Overall mood of the group or selected user.
            - <b>Group Toxicity Ratio</b>: Fraction of all messages that are toxic.
            """, unsafe_allow_html=True)
            st.info("A message is marked as 'toxic' if it contains words from a predefined abusive words list. You can extend this list in the code.")

        sentiment_df = sentiment_toxicity.user_sentiment_analysis(df if selected_user == 'Overall' else df[df['user'] == selected_user])
        toxicity_df = sentiment_toxicity.user_toxicity_analysis(df if selected_user == 'Overall' else df[df['user'] == selected_user])
        group_sent = sentiment_toxicity.group_sentiment_summary(df if selected_user == 'Overall' else df[df['user'] == selected_user])
        group_tox = sentiment_toxicity.group_toxicity_summary(df if selected_user == 'Overall' else df[df['user'] == selected_user])

        # --- Grouped Bar Chart for Sentiment ---
        if not sentiment_df.empty:
            sentiment_long = sentiment_df.melt(id_vars=['user'], value_vars=['positive_msgs', 'neutral_msgs', 'negative_msgs'],
                                               var_name='Sentiment', value_name='Count')
            sentiment_long['Sentiment'] = sentiment_long['Sentiment'].map({
                'positive_msgs': '😊 Positive',
                'neutral_msgs': '😐 Neutral',
                'negative_msgs': '😔 Negative'
            })
            fig_sent = px.bar(
                sentiment_long,
                x='user',
                y='Count',
                color='Sentiment',
                barmode='group',
                color_discrete_map={
                    '😊 Positive': '#4CAF50',
                    '😐 Neutral': '#3F51B5',
                    '😔 Negative': '#E6855E'
                },
                title='User-wise Sentiment Distribution',
                height=400
            )
            fig_sent.update_layout(
                paper_bgcolor='#1f2937',
                plot_bgcolor='#1f2937',
                font=dict(color='white'),
                legend_title_text='Sentiment',
                xaxis_title='User',
                yaxis_title='Message Count'
            )
            st.plotly_chart(fig_sent, use_container_width=True)

        # --- Donut Chart for Group Toxicity ---
        total_msgs = group_tox['total_msgs']
        toxic_msgs = int(group_tox['group_toxicity_ratio'] * total_msgs)
        clean_msgs = total_msgs - toxic_msgs
        donut_df = px.data.tips().iloc[:0].copy()  # empty df
        donut_df['Type'] = ['Toxic', 'Clean']
        donut_df['Count'] = [toxic_msgs, clean_msgs]
        donut_df = donut_df.iloc[:2].copy()
        donut_df['Type'] = ['🛑 Toxic', '✅ Clean']
        fig_donut = px.pie(
            donut_df,
            values='Count',
            names='Type',
            title='Group Toxicity Ratio',
            hole=0.5,
            color='Type',
            color_discrete_map={'🛑 Toxic': '#E53935', '✅ Clean': '#4CAF50'}
        )
        fig_donut.update_traces(textinfo='percent+label', pull=[0.1, 0], marker=dict(line=dict(color='#232946', width=2)))
        fig_donut.update_layout(
            paper_bgcolor='#1f2937',
            plot_bgcolor='#1f2937',
            font=dict(color='white'),
            showlegend=True,
            height=400
        )
        st.plotly_chart(fig_donut, use_container_width=True)

        # --- Group Summary Card ---
        st.markdown("<div style='display:flex;gap:2rem;margin-top:1.5rem;'>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style='background:#232946;padding:1.2rem 2rem;border-radius:12px;box-shadow:0 2px 8px #0002;min-width:260px;'>
            <div style='font-size:2.2rem;'>{'😊' if group_sent['group_sentiment_label']=='positive' else ('😔' if group_sent['group_sentiment_label']=='negative' else '😐')}</div>
            <div style='font-size:1.1rem;font-weight:bold;color:#4CAF50;'>Group Avg Sentiment</div>
            <div style='font-size:1.5rem;font-weight:bold;'>{group_sent['group_avg_sentiment']} ({group_sent['group_sentiment_label'].capitalize()})</div>
        </div>
        <div style='background:#232946;padding:1.2rem 2rem;border-radius:12px;box-shadow:0 2px 8px #0002;min-width:260px;'>
            <div style='font-size:2.2rem;'>{'🛑' if group_tox['group_toxicity_ratio']>0.1 else ('⚠️' if group_tox['group_toxicity_ratio']>0.02 else '✅')}</div>
            <div style='font-size:1.1rem;font-weight:bold;color:#E53935;'>Group Toxicity Ratio</div>
            <div style='font-size:1.5rem;font-weight:bold;'>{group_tox['group_toxicity_ratio']} (Total: {group_tox['total_msgs']})</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)