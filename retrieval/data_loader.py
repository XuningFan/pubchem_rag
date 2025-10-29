
import os
import gzip
from typing import Iterable, Dict, List
from html.parser import HTMLParser

class ParagraphExtractor(HTMLParser):
    def __init__(self, min_len: int = 40):
        super().__init__()
        self.min_len = min_len
        self._buf = []
        self._collected: List[str] = []
        self._capture = False
    def handle_starttag(self, tag, attrs):
        if tag in ("p","div","li","section"):
            self._buf = []
            self._capture = True
    def handle_endtag(self, tag):
        if tag in ("p","div","li","section"):
            self._capture = False
            paragraph = "".join(self._buf).strip()
            if len(paragraph) >= self.min_len:
                self._collected.append(paragraph)
            self._buf = []
    def handle_data(self, data):
        if self._capture:
            self._buf.append(data)
    def get_paragraphs(self) -> List[str]:
        return self._collected

def _read_plaintext(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()

def _read_gzip_tsv(path: str) -> List[Dict]:
    import csv
    rows = []
    with gzip.open(path, "rt", encoding="utf-8", errors="ignore") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            rows.append(row)
    return rows

def _html_to_paragraphs(path: str) -> List[str]:
    parser = ParagraphExtractor(min_len=40)
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        parser.feed(f.read())
    return parser.get_paragraphs()

def iter_raw_documents(raw_root: str) -> Iterable[Dict]:
    for root, dirs, files in os.walk(raw_root):
        for fn in files:
            path = os.path.join(root, fn)
            lower = fn.lower()

            # README / txt
            if lower.endswith(".txt") or "readme" in lower:
                try:
                    txt = _read_plaintext(path)
                    if len(txt.strip()) > 80:
                        yield {
                            "doc_id": f"{fn}",
                            "text": txt,
                            "source_path": path
                        }
                except Exception:
                    pass
                continue

            # HTML narrative docs
            if lower.endswith(".html") or lower.endswith(".htm"):
                try:
                    paras = _html_to_paragraphs(path)
                    for i, p in enumerate(paras):
                        yield {
                            "doc_id": f"{fn}::p{i}",
                            "text": p,
                            "source_path": path
                        }
                except Exception:
                    pass
                continue

            # gzipped TSV that *look* descriptive (*info)
            if lower.endswith(".gz") and ("info" in lower):
                try:
                    rows = _read_gzip_tsv(path)
                    candidate_cols = [
                        "description","summary","function","comment",
                        "mechanism","note","notes","role","pharmacology"
                    ]
                    for idx, row in enumerate(rows):
                        desc_bits = []
                        for col in candidate_cols:
                            if col in row and row[col]:
                                if len(row[col].strip()) > 40:
                                    desc_bits.append(row[col].strip())
                        if not desc_bits:
                            continue
                        text_block = "\n".join(desc_bits)
                        yield {
                            "doc_id": f"{fn}::row{idx}",
                            "text": text_block,
                            "source_path": path
                        }
                except Exception:
                    pass
                continue
