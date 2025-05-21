# WhatsApp Chat Analyzer 💬

A modern, interactive tool to analyze your WhatsApp group chats with beautiful visualizations, sentiment & toxicity detection, and deep insights into your conversations. Built with Python and Streamlit.

---

## ✨ Features

- **Chat Statistics:** Message counts, user activity, word/emoji usage, media/link sharing
- **Sentiment Analysis:** See the emotional tone of your group and each user
- **Toxicity Detection:** Identify toxic/abusive language and users
- **Topic Modeling:** Discover main discussion topics
- **Time Trends:** Visualize chat activity over days, weeks, and months
- **Responsive UI:** Works on desktop and mobile
- **No AI Summary:** (For privacy and cost reasons, no OpenAI/LLM summary is included)

---

## 🚀 Quick Start

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Rana-Zaeem/Whats_app_chat_analyzer.git
   cd Whats_app_chat_analyzer
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the app:**

   ```bash
   streamlit run app.py
   ```

4. **Export your WhatsApp chat:**
   - On your phone: Open chat → Menu (⋮) → More → Export chat → Without Media
   - Transfer the `.txt` file to your computer

5. **Upload and analyze:**
   - Open the app in your browser
   - Upload your exported chat file
   - Explore the dashboard and insights!

---

## 📊 Analysis Types

- **Chat Analysis:**
  - Message/user stats, word clouds, emoji usage, activity heatmaps
- **Sentiment & Toxicity:**
  - Per-user and group sentiment (positive/neutral/negative)
  - Toxic message/user detection (customizable word list)
- **Topic Analysis:**
  - Main topics and keywords in your group
- **Time Comparison:**
  - Compare chat activity across different periods

---

## 🖼️ Screenshots

*No screenshots are included in this repository. Run the app locally to see all visualizations and dashboards in action!*

---

## 🛡️ Privacy & Security

- All analysis runs **locally** on your machine
- No data is sent to any server or third party
- You control your chat data at all times

---

## ❓ FAQ

**Q: Does this use ChatGPT or OpenAI?**  
A: No. There is no AI summary or LLM integration for privacy and cost reasons. All analysis is statistical or rule-based.

**Q: Can I analyze any language?**  
A: Yes! Most features work for any language, but sentiment/toxicity is best for English/Hinglish.

**Q: Can I add my own toxic words?**  
A: Yes! Edit `models/sentiment_toxicity.py` to customize the toxic word list.

**Q: Is this free?**  
A: 100% free and open source.

---

## 🛠️ Tech Stack

- Python 3.8+
- Streamlit
- Pandas, Numpy, Matplotlib, Seaborn, Plotly
- NLTK, TextBlob, Gensim, spaCy
- WordCloud, urlextract, emoji

---

## 🤝 Contributing

Pull requests and suggestions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) or open an issue.

---

## 📄 License

MIT License. See [LICENSE](LICENSE).