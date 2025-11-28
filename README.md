# sqlite-rag-pipeline
An end-to-end Python pipeline that asynchronously scrapes websites, cleans the content, generates local vector embeddings, and stores them in a zero-dependency SQLite database for semantic search. No API keys required.

(SQLite + Crawl4AI)


# usage #

1. Run the Pipeline
This runs the Scraper, Processor, and a Test Search.
Modify TARGET_URLS in main.py to change what you scrape.
```
python main.py
```
Note: The first run will download the embedding model (~90MB).

2. Search the Knowledge Base
To perform a specific search query against your database:
```
python search.py
```
(Edit the q variable in search.py to change the question).

3. Visualise the Database
To see exactly what text was scraped and chunked:
```
python view_db.py
```
This will launch a browser window using D-Tale.


# Configuration #

Check config.py to tweak:

CHUNK_SIZE: How large text chunks should be.
MAX_CONCURRENT_REQUESTS: Speed of the scraper.
EMBEDDING_MODEL_NAME: Change the HuggingFace model.


# Project Structure #

scraper.py: Handles async web crawling.
processor.py: Cleans text and converts it to vectors.
database.py: Handles SQL read/write operations.
search.py: logic for cosine similarity calculation.


# Custom Search #
Open search.py in your editor. Change the bottom section:
```
if __name__ == "__main__":
    q = "Who invented deep learning?" # <--- Change this
    hits = search_knowledge_base(q)
    # ...
```

# Inspect Data #
```
python view_db.py
```
A D-Tale window will open in your browser.
Click on the raw_pages table to see the full scraped Markdown.

# Adding New Knowledge #

Open main.py.
Add a new URL to the TARGET_URLS list (e.g., a news article or documentation page).
Run python main.py again.
Efficiency Check: The script checks the database first. It will not rescrape URLs it already has, and it will only vectorize new pages.



