import streamlit as st
import time

def show_splash_screen(current_theme):
    """Display a splash screen animation for first-time visitors"""
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

def show_welcome_screen():
    """Display the welcome screen when no file is uploaded"""
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

def show_future_features():
    """Display future features information"""
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