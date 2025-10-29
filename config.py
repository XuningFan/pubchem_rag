
import os
from datetime import datetime

class Config:
    # paths
    DATA_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "data"))
    RAW_DIR = os.path.join(DATA_ROOT, "raw")
    CHUNK_DIR = os.path.join(DATA_ROOT, "chunks")
    SYNONYM_DIR = os.path.join(DATA_ROOT, "synonym")
    INDEX_DIR = os.path.join(DATA_ROOT, "index")
    LOG_DIR = os.path.join(DATA_ROOT, "logs")

    # retrieval
    TOP_K = 5
    CHUNK_SIZE = 1200
    CHUNK_OVERLAP = 200
    EMBEDDING_MODEL = "sentence-transformer-like-placeholder"
    FAISS_INDEX_FILE = os.path.join(INDEX_DIR, "faiss.index")
    FAISS_META_FILE  = os.path.join(INDEX_DIR, "meta.jsonl")

    # llm / generation
    LLM_ENDPOINT = "http://localhost:11434/api/generate"
    LLM_MODEL = "qwen2:30b"
    ANSWER_LANGUAGE = "English"

    # safety
    ENABLE_SAFETY_FILTER = True

    # logging
    RUN_ID = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    LOG_FILE = os.path.join(LOG_DIR, f"session_{RUN_ID}.jsonl")

    # eval
    MAX_GEN_TOKENS = 512
