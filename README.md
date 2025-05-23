# WhatsApp Chat Analyzer 💬

![GitHub license](https://img.shields.io/github/license/Rana-Zaeem/Whats_app_chat_analyzer)
![Python Version](https://img.shields.io/badge/python-3.10+-blue)
![Streamlit Version](https://img.shields.io/badge/streamlit-1.22.0-red)

WhatsApp Chat Analyzer is a modern, privacy-focused analytics tool for WhatsApp group and personal chats. It transforms exported chat data into actionable insights, interactive visualizations, and clear statistics—empowering you to understand your conversations at a glance.

---

## Key Features

- **Comprehensive Chat Statistics:**
  - Message counts, user activity, word and emoji usage, media/link sharing
  - Response time analysis and conversation flow metrics
- **Sentiment & Toxicity Analysis:**
  - Visualize emotional tone and detect negative language patterns
  - Identify toxic messages and users with customizable detection
- **Topic Modeling:**
  - Discover main discussion topics and keyword trends
- **Time Trends:**
  - Visualize chat activity by hour, day, week, and month
- **Interactive Visualizations:**
  - Word clouds, heatmaps, and dynamic charts
  - Filter by user, date range, or message type
- **Responsive UI:**
  - Clean, mobile-friendly design for all devices
- **Privacy by Design:**
  - All analysis runs locally—your data never leaves your computer

---

## Getting Started

### 1. Export Your WhatsApp Chat
- **Android:** Open chat → Menu (⋮) → More → Export chat → Without Media
- **iPhone:** Open chat → Tap group/contact name → Export Chat → Without Media
- Transfer the `.txt` file to your computer.

### 2. Install and Run the Analyzer
```bash
# Clone the repository
https://github.com/Rana-Zaeem/Whats_app_chat_analyzer.git
cd Whats_app_chat_analyzer

# (Optional) Create a virtual environment
python -m venv venv
# Activate (Windows)
venv\Scripts\activate
# Activate (macOS/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Launch the app
streamlit run app.py
```

### 3. Upload and Explore
- Open your browser at [http://localhost:8501](http://localhost:8501)
- Upload your exported chat file
- Explore the interactive dashboard and insights

---

## Analysis Modules

### Chat Overview
- Total messages, media, links, and unique users
- Most active users and message distribution
- Most used words and emoji
- Activity heatmaps and time trends

### Sentiment & Toxicity
- Emotional tone over time and by user
- Toxic message/user detection (customizable)

### Topic Modeling
- Main discussion topics and keyword trends
- Topic distribution over time

### Time Comparison
- Compare chat activity across different periods
- Analyze before/after events or group changes

---

## Technology Stack
- **Python 3.10+**
- **Streamlit** for the web interface
- **Pandas, NumPy** for data processing
- **Matplotlib, Seaborn, Plotly** for visualization
- **NLTK, TextBlob, scikit-learn** for NLP and analysis
- **WordCloud, urlextract, emoji** for additional features

---

## Privacy & Security
- All processing is local—no data is uploaded or shared
- No third-party APIs or cloud storage
- Open source: review and verify the code yourself

---

## License
This project is licensed under the MIT License.