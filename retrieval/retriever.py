
import os
import json
from typing import List, Dict
import numpy as np
from config import Config
from .index_builder import embed_text_batch
# import faiss

class Retriever:
    def __init__(self):
        self.meta = []
        with open(Config.FAISS_META_FILE, "r", encoding="utf-8") as f:
            for line in f:
                self.meta.append(json.loads(line))

        vec_path = os.path.join(Config.INDEX_DIR, "vectors.npy")
        self.vecs = np.load(vec_path)  # shape [N, dim]

    def search(self, query: str, top_k: int = None) -> List[Dict]:
        if top_k is None:
            top_k = Config.TOP_K

        q_vec = np.array(embed_text_batch([query])[0], dtype="float32").reshape(1,-1)
        scores = (q_vec @ self.vecs.T).flatten()  # cosine if normalized

        idxs = np.argsort(-scores)[:top_k]

        results = []
        for rank, idx in enumerate(idxs):
            m = self.meta[idx]
            results.append({
                "rank": int(rank),
                "score": float(scores[idx]),
                "text": m["text"],
                "source_id": m["source_doc_id"],
            })
        return results
