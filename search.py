# --- search.py ---
import sqlite3
import json
import numpy as np
from sentence_transformers import SentenceTransformer
from config import DB_NAME, EMBEDDING_MODEL_NAME

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def search_knowledge_base(query, top_k=3):
    print(f"🔎 Searching for: '{query}'...")
    model = SentenceTransformer(EMBEDDING_MODEL_NAME)
    query_vector = model.encode(query)
    
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT chunk_text, embedding_json, source_url FROM knowledge_vectors")
    rows = c.fetchall()
    conn.close()
    
    results = []
    for row in rows:
        db_vector = json.loads(row['embedding_json'])
        score = cosine_similarity(query_vector, db_vector)
        results.append({"score": score, "text": row['chunk_text'], "url": row['source_url']})
    
    results.sort(key=lambda x: x['score'], reverse=True)
    return results[:top_k]

if __name__ == "__main__":
    # Test Question
    q = "What is a large language model?"
    hits = search_knowledge_base(q)
    
    print(f"\n--- Results for: {q} ---")
    for hit in hits:
        print(f"\n[Score: {hit['score']:.4f}] from {hit['url']}")
        print(f"Content: {hit['text']}")