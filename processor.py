# --- processor.py ---
import re
from sentence_transformers import SentenceTransformer
from database import fetch_unprocessed_pages, save_vector_chunk
from config import CHUNK_SIZE, CHUNK_OVERLAP, EMBEDDING_MODEL_NAME

def clean_noise(text):
    """Aggressive cleaning to remove Wikipedia boilerplate."""
    if not text: return ""
    
    # Remove Markdown images and links
    text = re.sub(r'!\[[^\]]*\]\([^)]+\)', '', text) # Images
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text) # Links (keep text)
    text = re.sub(r'\[\d+\]', '', text) # Citations [1]
    
    # Remove specific Wikipedia Noise patterns
    junk = [
        r'Jump to content', r'Jump to search', r'Donate', r'Log in', 
        r'Create account', r'Personal tools', r'Toggle the table of contents'
    ]
    for pattern in junk:
        text = re.sub(pattern, '', text, flags=re.IGNORECASE)
    
    # Collapse whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def smart_chunking(text):
    """Splits text by sentences, grouping them into chunks."""
    # Split by sentence endings (.?!)
    sentences = re.split(r'(?<=[.?!])\s+', text)
    
    chunks = []
    current_chunk = []
    current_len = 0
    
    for sentence in sentences:
        if current_len + len(sentence) > CHUNK_SIZE and current_chunk:
            chunks.append(" ".join(current_chunk))
            # Start new chunk with overlap (keep last sentence)
            current_chunk = current_chunk[-1:]
            current_len = len(current_chunk[0])
        
        current_chunk.append(sentence)
        current_len += len(sentence)
    
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    return chunks

def run_processor():
    print("🧠 Loading AI Model (this happens once)...")
    model = SentenceTransformer(EMBEDDING_MODEL_NAME)
    
    pages = fetch_unprocessed_pages()
    print(f"📚 Found {len(pages)} new pages to vectorize.")
    
    for page in pages:
        url = page['url']
        raw_text = page['markdown']
        
        # 1. Clean
        clean_text = clean_noise(raw_text)
        
        # 2. Chunk
        chunks = smart_chunking(clean_text)
        
        # 3. Embed
        if chunks:
            vectors = model.encode(chunks)
            
            # 4. Save
            for chunk_text, vector in zip(chunks, vectors):
                save_vector_chunk(url, chunk_text, vector.tolist())
                
            print(f"💾 Processed {len(chunks)} chunks for: {url}")
    
    print("✨ Processing Complete.")