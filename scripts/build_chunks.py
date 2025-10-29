
import os
import json
from config import Config
from retrieval.data_loader import iter_raw_documents
from retrieval.chunker import chunk_document

def main():
    os.makedirs(Config.CHUNK_DIR, exist_ok=True)
    out_file = os.path.join(Config.CHUNK_DIR, "chunks.jsonl")

    with open(out_file, "w", encoding="utf-8") as out_f:
        for doc in iter_raw_documents(Config.RAW_DIR):
            chunks = chunk_document(doc)
            for ch in chunks:
                out_f.write(json.dumps(ch, ensure_ascii=False) + "\n")

    print(f"[build_chunks] Wrote chunks to {out_file}")

if __name__ == "__main__":
    main()
