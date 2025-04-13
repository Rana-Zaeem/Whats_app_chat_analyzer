mkdir -p ~/.streamlit/

python -m nltk.downloader -d /app/nltk_data punkt stopwords
python -m spacy download --no-deps en_core_web_sm