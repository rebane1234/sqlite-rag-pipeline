# --- scraper.py ---
import asyncio
from crawl4ai import AsyncWebCrawler
from tenacity import retry, stop_after_attempt, wait_exponential
from database import save_raw_page
from config import MAX_CONCURRENT_REQUESTS, USER_AGENT

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
async def scrape_one(crawler, url, semaphore):
    async with semaphore:
        print(f"🕸️  Scraping: {url}")
        
        # 'div.mw-parser-output' is specific to Wikipedia to get ONLY the article body.
        # If scraping other sites, change this to 'main', 'article', or 'body'.
        result = await crawler.arun(
            url=url, 
            css_selector="div.mw-parser-output",
            word_count_threshold=50
        )
        
        if result.success:
            save_raw_page({
                "url": url,
                "title": result.media.get("title", "Unknown"),
                "content": result.markdown
            })
            print(f"✅ Saved: {url}")
        else:
            print(f"❌ Failed: {url} - {result.error_message}")

async def run_scraper(urls):
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)
    print(f"🚀 Starting Scraper on {len(urls)} URLs...")
    
    async with AsyncWebCrawler(verbose=False, user_agent=USER_AGENT) as crawler:
        tasks = [scrape_one(crawler, url, semaphore) for url in urls]
        await asyncio.gather(*tasks)