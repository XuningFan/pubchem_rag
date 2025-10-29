
import os
import json
from typing import List, Dict
from config import Config
import numpy as np
# import faiss  # when ready

def embed_text_batch(text_list: List[str]) -> List[List[float]]:
    dim = 384  # placeholder dimension
    vecs = np.random.randn(len(text_list), dim).astype("float32")
    norms = np.linalg.norm(vecs, axis=1, keepdims=True) + 1e-9
    vecs = vecs / norms
    return vecs.tolist()

def build_faiss_index(chunks: List[Dict]):
    os.makedirs(Config.INDEX_DIR, exist_ok=True)

    texts = [c["text"] for c in chunks]
    vecs = embed_text_batch(texts)
    vecs_np = np.array(vecs, dtype="float32")
    dim = vecs_np.shape[1]

    # index = faiss.IndexFlatIP(dim)
    # index.add(vecs_np)
    # faiss.write_index(index, Config.FAISS_INDEX_FILE)

    meta_path = Config.FAISS_META_FILE
    with open(meta_path, "w", encoding="utf-8") as mf:
        for ch in chunks:
            mf.write(json.dumps(ch, ensure_ascii=False) + "\n")

    tmp_vecfile = os.path.join(Config.INDEX_DIR, "vectors.npy")
    np.save(tmp_vecfile, vecs_np)

    print("[build_faiss_index] wrote:")
    print(" - meta:", meta_path)
    print(" - vectors:", tmp_vecfile)
    print(" - (FAISS index writing is TODO)")
