
import os
import json
from typing import Optional

class SynonymIndex:
    def __init__(self, synonym_file: str):
        self.term2cid = {}
        if os.path.exists(synonym_file):
            with open(synonym_file, "r", encoding="utf-8") as f:
                for line in f:
                    row = json.loads(line)
                    self.term2cid[row["term"]] = row["cid"]

    def lookup_cid(self, user_term: str) -> Optional[int]:
        key = user_term.strip().lower()
        return self.term2cid.get(key, None)
