import streamlit as st
import pandas as pd
import nltk

# Configure page
st.set_page_config(
    page_title="WhatsApp Chat Analyzer (Minimal)",
    page_icon="💬",
    layout="wide",
)

# Download NLTK data in a non-blocking way
try:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
except:
    pass

# Main app
st.title("WhatsApp Chat Analyzer")
st.write("This is a minimal version to test deployment")

# Simple form
with st.form("chat_form"):
    uploaded_file = st.file_uploader("Choose a WhatsApp chat export file")
    submit_button = st.form_submit_button("Analyze")

    if submit_button and uploaded_file is not None:
        # Try to read the file
        try:
            content = uploaded_file.getvalue().decode("utf-8")
            st.success(f"Successfully loaded file with {len(content)} characters")
            
            # Display sample of content
            st.text("Preview of chat content:")
            st.code(content[:500] + "...")
        except Exception as e:
            st.error(f"Error processing file: {e}")
    
# Footer
st.markdown("---")
st.caption("WhatsApp Chat Analyzer - Minimal Version for Deployment Testing")
