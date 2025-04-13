mkdir -p ~/.streamlit/
mkdir -p ~/.nltk_data

echo "\
[server]\n\
port = $PORT\n\
enableCORS = false\n\
headless = true\n\
\n\
" > ~/.streamlit/config.toml

python -m nltk.downloader punkt
python -m nltk.downloader stopwords
python -m spacy download en_core_web_sm