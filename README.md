
# PubChem RAG Assistant (safety-aware)

## What this is
A local Retrieval-Augmented Generation (RAG) assistant focused on chemical / pharmacology queries.
It:
- Uses your local snapshot of PubChem-like descriptive text (README, info summaries, etc.).
- Enriches answers with on-demand PubChem API fields (formula, MW, pharmacology, targets, safety).
- Enforces safety: no synthesis steps, no lab protocols, no misuse guidance.
- Logs all Q&A locally for reproducibility and eval.

Answers are in English, scientific/neutral tone.

## Directory layout
- `config.py` : global config (paths, model, safety flags)
- `main.py`   : interactive REPL
- `retrieval/`: chunking, embedding, index building, semantic retrieval
- `api/`      : PubChem API fetch + summarization
- `rag/`      : prompt building and LLM call
- `scripts/`  : data prep scripts
- `eval/`     : evaluation tools
- `data/`     : your local data (not fully in git)

### data/ subdirs
- `data/raw/`     : your downloaded PubChem sources
- `data/chunks/`  : processed narrative chunks (`chunks.jsonl`)
- `data/synonym/` : synonym → CID (`synonyms.jsonl`)
- `data/index/`   : vectors / FAISS index / meta.jsonl
- `data/logs/`    : session logs

## Setup

### 1. Install deps
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Local LLM via Ollama
```bash
ollama pull qwen2:30b
ollama serve
```
Make sure `config.py` has:
```python
LLM_ENDPOINT = "http://localhost:11434/api/generate"
LLM_MODEL = "qwen2:30b"
```

### 3. Put PubChem-derived sources into `data/raw/`
Copy the files you downloaded (README-like text, *_info.gz, pug-rest.html, pug-view.html, etc.).
We embed only narrative/annotated text. Pure mapping tables stay out of embeddings.

### 4. Build narrative chunks
```bash
python scripts/build_chunks.py
```

### 5. Build synonym dictionary
```bash
python scripts/build_synonyms.py
```

### 6. Build vector index
```bash
python scripts/build_index.py
```

### 7. Run assistant (REPL)
```bash
python main.py
```

Ask things like:
```text
>>> PubChem中苯的分子式和重量是什么？
```

Internal flow:
1. Extract candidate compound term(s) from query, resolve to CID via synonym index.
2. Fetch PubChem API info (formula, MW, mechanism, safety).
3. Retrieve top-k semantic chunks from local index.
4. Build safety-aware prompt.
5. Generate answer with local LLM.
6. Log to `data/logs/session_*.jsonl`.

### 8. Eval
Prepare `eval/evalset.jsonl` similar to `eval/evalset.example.jsonl` and run:
```bash
python -m eval.tests
```

## Safety policy
- No synthesis routes, no lab protocols, no dosing optimization, no weaponization.
- High-level pharmacology / toxicology context is OK.
- All interactions are logged locally. Do not publish logs containing sensitive requests.

## Next steps / TODO
- Implement real embeddings + FAISS instead of random vectors.
- Finish `fetch_compound_info_by_name()` in `api/pubchem_api.py`.
- Finish synonym cleaner + synonym fetcher in `scripts/build_synonyms.py`.
- Improve name resolution / fuzzy match for multilingual compound names.
