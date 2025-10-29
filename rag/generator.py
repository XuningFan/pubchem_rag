
import json
import requests
from config import Config

def generate_answer(prompt: str) -> str:
    payload = {
        "model": Config.LLM_MODEL,
        "prompt": prompt,
        "options": {
            "num_predict": Config.MAX_GEN_TOKENS
        }
    }
    r = requests.post(Config.LLM_ENDPOINT, json=payload, timeout=120)
    r.raise_for_status()

    try:
        data = r.json()
        answer = data.get("response", "")
    except json.JSONDecodeError:
        answer = r.text
    return answer.strip()
