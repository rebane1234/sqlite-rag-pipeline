# --- main.py ---
import asyncio
from database import init_db
from scraper import run_scraper
from processor import run_processor
from search import search_knowledge_base

# DEFINE YOUR TARGETS HERE
TARGET_URLS = [
    "https://en.wikipedia.org/wiki/Artificial_intelligence",
    "https://en.wikipedia.org/wiki/Machine_learning",
    "https://en.wikipedia.org/wiki/Deep_learning",
    "https://en.wikipedia.org/wiki/Generative_artificial_intelligence",
    "https://en.wikipedia.org/wiki/Large_language_model"
]

def main():
    print("=======================================")
    print("       INGESTION PIPELINE v2.0         ")
    print("=======================================")

    # 1. Setup DB
    init_db()

    # 2. Run Scraper (Async)
    try:
        asyncio.run(run_scraper(TARGET_URLS))
    except KeyboardInterrupt:
        print("Scraping stopped.")

    # 3. Run Processor (Cleaning + Embedding)
    run_processor()

    print("\n=======================================")
    print("   PIPELINE FINISHED. RUNNING TEST.    ")
    print("=======================================")
    
    # 4. Auto-Test Search
    results = search_knowledge_base("How do LLMs use transformers?")
    for res in results:
        print(f"\n> {res['text']} \n(Source: {res['url']})")

if __name__ == "__main__":
    main()
