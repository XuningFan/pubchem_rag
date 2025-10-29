
import json
import os
from typing import Any, Dict
from config import Config

os.makedirs(Config.LOG_DIR, exist_ok=True)

def log_interaction(record: Dict[str, Any]):
    with open(Config.LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
