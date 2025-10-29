
from typing import List, Dict
from config import Config

def chunk_document(doc: Dict) -> List[Dict]:
    text = doc["text"]
    chunks = []
    size = Config.CHUNK_SIZE
    overlap = Config.CHUNK_OVERLAP

    start = 0
    chunk_i = 0
    while start < len(text):
        end = start + size
        chunk_txt = text[start:end]
        chunks.append({
            "chunk_id": f"{doc['doc_id']}::chunk{chunk_i}",
            "text": chunk_txt,
            "source_doc_id": doc["doc_id"],
        })
        start = end - overlap
        if start < 0:
            break
        chunk_i += 1
        if start >= len(text):
            break
    return chunks
