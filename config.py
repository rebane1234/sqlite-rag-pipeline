# --- config.py ---
import os

# Database File
DB_NAME = "ai_knowledge_base.db"

# Scraper Settings
# How many tabs to open at once (Increase if you have fast internet/CPU)
MAX_CONCURRENT_REQUESTS = 3
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

# Processor Settings
# Approx 3-5 sentences per chunk
CHUNK_SIZE = 500 
CHUNK_OVERLAP = 50

# AI Model Settings
# Small, fast, effective. Downloads automatically (~90MB).
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"

# Suppress the Windows Symlink warning
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"