# WhatsApp Chat Analyzer 💬

![GitHub license](https://img.shields.io/github/license/Rana-Zaeem/Whats_app_chat_analyzer)
![Python Version](https://img.shields.io/badge/python-3.8+-blue)
![Streamlit Version](https://img.shields.io/badge/streamlit-1.15.0-red)

A powerful, interactive tool to analyze your WhatsApp conversations with beautiful visualizations, sentiment analysis, and deep insights. Discover patterns, trends, and statistics from your personal or group chats. Built with Python and Streamlit.

> 📱 **Privacy First:** All analysis happens locally on your machine. Your chats never leave your computer.

---

## ✨ Features

- **Complete Chat Statistics:** 
  - Message counts, user participation, peak activity times
  - Word usage, emoji frequency, media/link sharing analysis
  - Response time patterns and conversation flow metrics

- **Advanced Analytics:**
  - **Sentiment Analysis:** Track emotional tone over time and by user
  - **Toxicity Detection:** Identify negative language patterns
  - **Topic Modeling:** Discover what your group talks about most
  - **Time Trends:** Visualize activity patterns by hour, day, week, month

- **Interactive Visualizations:**
  - Beautiful charts, word clouds, and heat maps
  - Filter data by date range, user, or message type
  - Compare different time periods side-by-side

- **User-friendly Interface:**
  - Clean, responsive design that works on all devices
  - Easy navigation between different analysis sections
  - Fast performance even with large chat histories

---

## 🚀 Quick Start

### Option 1: Try the Live Demo
Visit our hosted version at [WhatsApp Analyzer App](https://whatsapp-chat-analyzer.streamlit.app/) *(URL example - update with your actual deployment URL)*

### Option 2: Run Locally

1. **Export your WhatsApp chat:**
   - **Android:** Open chat → Menu (⋮) → More → Export chat → Without Media
   - **iPhone:** Open chat → Tap on group/contact name → Export Chat → Without Media
   - Transfer the `.txt` file to your computer

2. **Clone the repository:**

   ```bash
   git clone https://github.com/Rana-Zaeem/Whats_app_chat_analyzer.git
   cd Whats_app_chat_analyzer
   ```

3. **Set up environment:**
   ```bash
   # Create a virtual environment (optional but recommended)
   python -m venv venv
   
   # Activate the environment
   # For Windows:
   venv\Scripts\activate
   # For macOS/Linux:
   source venv/bin/activate
   
   # Install dependencies
   pip install -r requirements.txt
   ```

4. **Run the app:**
   ```bash
   streamlit run app.py
   ```

5. **Upload and analyze:**
   - Open your browser at http://localhost:8501
   - Upload your exported chat file
   - Explore the interactive dashboard!

---

## 📊 What You Can Analyze

### Chat Analysis Dashboard
- **Overview Statistics:** Total messages, media, links, unique users
- **User Engagement:** Most active members, message distribution
- **Content Analysis:** 
  - Most used words (with customizable stopwords)
  - Emoji frequency and usage patterns
  - URL and media sharing patterns
- **Activity Patterns:** Peak hours, busiest days, monthly trends

### Sentiment & Toxicity Analysis
- **Emotional Trends:** Track how conversation tone changes over time
- **User Sentiment Profiles:** See which members are more positive/negative
- **Toxicity Detection:** Identify aggressive/toxic language
- **Custom Detection:** Modify words/phrases considered as toxic

### Topic Modeling
- **Key Topics:** Discover main conversation themes automatically
- **Keyword Analysis:** Most significant terms per topic
- **Topic Distribution:** How conversation subjects evolve over time

### Time Comparison
- **Side-by-side Analysis:** Compare different chat periods
- **Before/After Events:** Analyze how discussions changed after specific events
- **Growth Patterns:** Track how group activity has changed over time

---

## 🖼️ Screenshots

*For privacy reasons, screenshots with actual chat data are not included in this repository. Run the app locally to see all visualizations and dashboards in action with your own data!*

---

## 🛡️ Privacy & Security

- **100% Local Processing:** All analysis runs on your machine only
- **No Cloud Storage:** Your chat data is never uploaded or stored online
- **No API Dependencies:** No external services access your conversations
- **Open Source:** All code is transparent and can be reviewed

---

## ❓ FAQ

**Q: Does this use ChatGPT or OpenAI?**  
A: No. There is no AI summary or LLM integration for privacy and cost reasons. All analysis is statistical or rule-based.

**Q: Can I analyze chats in languages other than English?**  
A: Yes! The core analysis features work for any language. Sentiment and topic analysis work best with English and Hinglish, but will still provide insights for other languages.

**Q: How large a chat history can this handle?**  
A: The analyzer can process group chats with tens of thousands of messages. For very large chats (100,000+ messages), processing might take a few minutes.

**Q: Can I customize the toxic words detection?**  
A: Yes! Edit `models/sentiment_toxicity.py` to customize the toxic word list. See our [CONTRIBUTING.md](CONTRIBUTING.md) for detailed instructions.

**Q: Will this work with my business WhatsApp chats?**  
A: Yes, both personal and business WhatsApp exports are supported.

**Q: Is this app free to use?**  
A: 100% free and open source. There are no paid features or subscriptions.

**Q: Do I need to be online to use the analyzer?**  
A: Once the app is running locally, you don't need internet access to analyze your chats.

---

## 🛠️ Tech Stack

- **Core:** Python 3.8+, Streamlit
- **Data Processing:** Pandas, NumPy
- **Visualization:** Matplotlib, Seaborn, Plotly
- **NLP & Analysis:** NLTK, TextBlob, scikit-learn
- **Utilities:** WordCloud, urlextract, emoji

---

## 🤝 Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to help improve this project.

---

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🙏 Acknowledgments

- Thanks to all contributors who have helped improve this project
- Built with [Streamlit](https://streamlit.io/) 
- Uses [TextBlob](https://textblob.readthedocs.io/) for sentiment analysis
- Inspired by the need for better WhatsApp chat insights

---

## 🤝 Contributing

Pull requests and suggestions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) or open an issue.

---

## 📄 License

MIT License. See [LICENSE](LICENSE).