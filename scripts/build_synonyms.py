
import os
import json
from typing import List
from config import Config

# NOTE: You'll need requests+pandas etc if you do fancy stuff.

def load_seed_cids() -> List[int]:
    # TODO: replace with your real CID set (e.g. approved drugs etc.)
    return [2244]  # aspirin demo

def fetch_synonyms_for_cid(cid: int):
    # TODO: call PubChem /synonyms/JSON similar to api/pubchem_api._fetch_synonyms
    # return list of raw synonym strings
    raise NotImplementedError

def clean_synonym(term: str) -> str:
    # TODO: lowercase, strip ®™©, drop CAS-like strings, trim salt suffixes
    raise NotImplementedError

def main():
    os.makedirs(Config.SYNONYM_DIR, exist_ok=True)
    out_file = os.path.join(Config.SYNONYM_DIR, "synonyms.jsonl")

    with open(out_file, "w", encoding="utf-8") as out_f:
        for cid in load_seed_cids():
            raw_syns = fetch_synonyms_for_cid(cid)
            cleaned_terms = []
            for s in raw_syns:
                cs = clean_synonym(s)
                if cs:
                    cleaned_terms.append(cs)

            seen = set()
            final_terms = []
            for t in cleaned_terms:
                if t not in seen:
                    final_terms.append(t)
                    seen.add(t)
                if len(final_terms) >= 10:
                    break

            for t in final_terms:
                row = {"term": t, "cid": cid}
                out_f.write(json.dumps(row, ensure_ascii=False) + "\n")

    print(f"[build_synonyms] Wrote synonym index to {out_file}")

if __name__ == "__main__":
    main()
