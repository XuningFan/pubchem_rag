
import os
import json
from typing import List, Dict
from config import Config
from retrieval.index_builder import build_faiss_index

def load_chunks() -> List[Dict]:
    chunks_path = os.path.join(Config.CHUNK_DIR, "chunks.jsonl")
    chunks = []
    with open(chunks_path, "r", encoding="utf-8") as f:
        for line in f:
            chunks.append(json.loads(line))
    return chunks

def main():
    os.makedirs(Config.INDEX_DIR, exist_ok=True)
    chunks = load_chunks()
    build_faiss_index(chunks)
    print(f"[build_index] Index written to {Config.FAISS_INDEX_FILE}")

if __name__ == "__main__":
    main()
