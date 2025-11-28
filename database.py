# --- database.py ---
import sqlite3
import json
from config import DB_NAME

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # 1. Raw Data Table (Idempotent: URL is Primary Key)
    c.execute('''
        CREATE TABLE IF NOT EXISTS raw_pages (
            url TEXT PRIMARY KEY,
            title TEXT,
            markdown TEXT,
            scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # 2. Vector Storage Table
    # We store the vector as a JSON string because SQLite is simple
    c.execute('''
        CREATE TABLE IF NOT EXISTS knowledge_vectors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_url TEXT,
            chunk_text TEXT,
            embedding_json TEXT, 
            FOREIGN KEY(source_url) REFERENCES raw_pages(url)
        )
    ''')
    conn.commit()
    conn.close()

def save_raw_page(data):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    try:
        c.execute('INSERT OR REPLACE INTO raw_pages (url, title, markdown) VALUES (?, ?, ?)',
                  (data['url'], data['title'], data['content']))
        conn.commit()
    except Exception as e:
        print(f"Error saving raw page: {e}")
    finally:
        conn.close()

def save_vector_chunk(url, text, vector):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    vector_str = json.dumps(vector)
    c.execute('INSERT INTO knowledge_vectors (source_url, chunk_text, embedding_json) VALUES (?, ?, ?)',
              (url, text, vector_str))
    conn.commit()
    conn.close()

def fetch_unprocessed_pages():
    """Finds pages we scraped but haven't vectorized yet."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('''
        SELECT * FROM raw_pages 
        WHERE url NOT IN (SELECT DISTINCT source_url FROM knowledge_vectors)
    ''')
    return c.fetchall()