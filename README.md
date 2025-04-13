# WhatsApp Chat Analyzer

📱 A powerful Python-based WhatsApp chat analyzer that provides deep insights into your conversations through interactive visualizations. Features include message pattern analysis, sentiment analysis, topic modeling, and detailed activity metrics. Built with Streamlit for an easy-to-use web interface.

🚀 **Key Features:**
- Advanced message analytics and statistics
- Sentiment analysis of conversations
- Topic modeling to identify discussion themes
- Interactive visualizations and word clouds
- Support for individual and group chats

## Features

### 1. Basic Chat Analysis
- Total message count and word count
- Media and links shared analysis
- Most active users identification
- Word cloud visualization
- Common words analysis
- Emoji analysis with distribution

### 2. Temporal Analysis
- Monthly message timeline
- Daily activity patterns
- Weekly activity heatmap
- Response time analysis
- Hourly activity distribution

### 3. Sentiment Analysis
- Message sentiment classification (Positive, Negative, Neutral)
- Sentiment trends over time
- Sentiment distribution visualization
- Sentiment-based word clouds

### 4. Topic Analysis
- Automatic topic detection
- Topic strength visualization
- Key words per topic
- Topic distribution over time

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Rana-Zaeem/Whats_app_chat_analyzer.git
cd whats_app_chat_analyzer
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run app.py
```

## How to Use

1. Export your WhatsApp chat:
   - Open WhatsApp chat
   - Click on three dots (⋮)
   - More > Export chat
   - Choose 'Without Media'

2. Upload the exported text file to the application

3. Select analysis type:
   - Chat Analysis
   - Sentiment Analysis
   - Topic Analysis

4. Explore various visualizations and insights

## Technology Stack

- Python 3.x
- Streamlit
- Pandas
- NLTK
- Plotly
- WordCloud
- Matplotlib
- Seaborn
- Scikit-learn

## Requirements

All required packages are listed in `requirements.txt`. Key dependencies include:
- streamlit
- pandas
- numpy
- matplotlib
- seaborn
- plotly
- wordcloud
- nltk
- scikit-learn
- emoji

## Project Structure

```
whats_app_chat_analyzer/
│
├── app.py              # Main application file
├── preprocessor.py     # Data preprocessing module
├── helper.py          # Helper functions
├── sentiment.py       # Sentiment analysis module
├── topic_analysis.py  # Topic analysis module
├── requirements.txt   # Project dependencies
├── stop_hinglish.txt # Custom stopwords
└── README.md         # Project documentation
```

## Features in Detail

### Chat Analysis
- Message count statistics
- User participation analysis
- Temporal patterns
- Word frequency analysis
- Emoji usage patterns
- Media sharing patterns
- Link sharing analysis
- Response time analysis

### Sentiment Analysis
- Message sentiment classification
- Sentiment trends
- Emotional pattern detection
- Positive/Negative word clouds
- Sentiment distribution

### Topic Analysis
- Automated topic detection
- Topic visualization
- Key terms extraction
- Topic evolution over time

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License, which means:

### What you can do:
- ✓ Commercial use
- ✓ Modify the code
- ✓ Distribute the code
- ✓ Use privately
- ✓ Use in closed source projects

### Requirements:
- Include the original copyright notice
- Include the MIT License text in any significant portion of the code

The MIT License is a permissive license that is short and to the point. It lets people do almost anything they want with your project, like making and distributing closed source versions, as long as they provide a copy of the MIT License terms and the copyright notice.

## Acknowledgments

- Thanks to Streamlit for the awesome framework
- WhatsApp for the chat export feature
- All contributors and users of this project