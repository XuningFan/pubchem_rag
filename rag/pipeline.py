
import re
from config import Config
from retrieval.synonym_index import SynonymIndex
from retrieval.retriever import Retriever
from api.pubchem_api import fetch_compound_info_by_cid, fetch_compound_info_by_name
from api.enrich import summarize_api_info
from rag.prompt_template import build_prompt
from rag.generator import generate_answer
from safety import needs_strict_safety
from logging_utils import log_interaction

def guess_compound_terms(user_query: str):
    tokens = re.findall(r"[\u4e00-\u9fa5]+|[A-Za-z0-9\-\+\._]+", user_query)
    ban = {"pubchem","中","的","分子式","和","重量","是什么"}
    candidates = [t for t in tokens if t not in ban]
    return candidates

class RAGPipeline:
    def __init__(self):
        self.syn = SynonymIndex(
            synonym_file=f"{Config.SYNONYM_DIR}/synonyms.jsonl"
        )
        self.retriever = Retriever()

    def _resolve_compound(self, user_query: str):
        cid = None
        term_for_api = None

        for term in guess_compound_terms(user_query):
            c = self.syn.lookup_cid(term)
            if c is not None:
                cid = c
                term_for_api = term
                break

        if cid is None and term_for_api is None:
            cands = guess_compound_terms(user_query)
            if len(cands) > 0:
                term_for_api = cands[0]

        return cid, term_for_api

    def run(self, user_query: str, top_k: int = None) -> str:
        cid, compound_term = self._resolve_compound(user_query)

        raw_api = None
        if cid is not None:
            raw_api = fetch_compound_info_by_cid(cid)
        elif compound_term is not None:
            raw_api = fetch_compound_info_by_name(compound_term)

        api_summary = summarize_api_info(raw_api) if raw_api else {}

        hits = self.retriever.search(user_query, top_k=top_k)

        strict = needs_strict_safety(user_query) if Config.ENABLE_SAFETY_FILTER else False
        prompt = build_prompt(
            user_query=user_query,
            retrieved_docs=hits,
            api_info_summary=api_summary,
            strict_safety=strict
        )

        answer = generate_answer(prompt)

        log_interaction({
            "user_query": user_query,
            "resolved_cid": cid,
            "resolved_term": compound_term,
            "retrieved_docs": hits,
            "api_info": api_summary,
            "final_answer": answer
        })

        return answer
