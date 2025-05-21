import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time

def run_time_comparison(selected_user, df):
    """Handle time comparison visualization and UI"""
    # Display the header section
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
            
            # Get current theme colors
            current_theme = {
                'secondary': '#3B88C3',
                'accent': '#E6855E',
                'primary': '#4CAF50'
            }
            
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