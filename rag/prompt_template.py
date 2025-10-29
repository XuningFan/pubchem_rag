
from typing import List, Dict
from safety import safety_prefix

BASE_STYLE = (
    "You are a biomedical/cheminformatics assistant. "
    "Answer in English with a concise academic tone. "
    "Focus on high-level pharmacology, mechanism, biological targets, "
    "and known safety considerations.\n"
    "Do not provide experimental procedures, lab steps, synthesis routes, "
    "dose optimization guidance, or instructions that could enable harm.\n"
)

def build_prompt(user_query: str,
                 retrieved_docs: List[Dict],
                 api_info_summary: Dict,
                 strict_safety: bool) -> str:

    context_blocks = []
    for doc in retrieved_docs:
        context_blocks.append(
            f"[SOURCE {doc['source_id']}] {doc['text']}"
        )

    api_block = ""
    if api_info_summary:
        api_block = (
            "API_SUMMARY:\n"
            f"Name: {api_info_summary.get('canonical_name','')}\n"
            f"Mechanism: {api_info_summary.get('mechanism_summary','')}\n"
            f"Targets: {api_info_summary.get('target_summary','')}\n"
            f"Safety: {api_info_summary.get('safety_summary','')}\n"
            f"Formula: {api_info_summary.get('props',{}).get('formula','')}\n"
            f"MW: {api_info_summary.get('props',{}).get('mw','')}\n"
        )

    prompt = (
        safety_prefix(strict_safety)
        + BASE_STYLE
        + "\nCONTEXT DOCUMENTS:\n"
        + "\n\n".join(context_blocks[:10])
        + "\n\n"
        + api_block
        + "\nUSER QUESTION:\n"
        + user_query
        + "\n\n"
        "TASK:\n"
        "Produce an evidence-based answer. If information is uncertain or "
        "not found in the provided context or API summary, explicitly say "
        "that evidence is limited.\n"
    )
    return prompt
