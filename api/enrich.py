
from typing import Dict, Any

def _safe_join(parts):
    return " ".join([p for p in parts if p]).strip()

def summarize_api_info(raw: Dict[str, Any]) -> Dict[str, Any]:
    if not raw:
        return {}

    cid = raw.get("cid")
    names = raw.get("names", {})
    props = raw.get("properties", {})
    pharm = raw.get("pharmacology")
    mech  = raw.get("mechanism")
    targets = raw.get("targets", [])
    safety = raw.get("safety", {})

    canonical_name = names.get("canonical") or f"CID {cid}"

    desc_bits = []
    if pharm:
        desc_bits.append(pharm)
    elif mech:
        desc_bits.append(mech)
    short_description = _safe_join(desc_bits)
    if not short_description:
        short_description = f"{canonical_name} is a chemical entry in PubChem."

    mechanism_summary = mech or ""
    target_summary = ""
    if targets:
        target_summary = "Key biological targets include: " + ", ".join(targets)

    tox = safety.get("toxicology_summary")
    haz = safety.get("hazard_statements", [])
    safety_summary = ""
    if tox:
        safety_summary += tox
    if haz:
        if safety_summary:
            safety_summary += " "
        safety_summary += "Reported hazard statements include: " + "; ".join(haz[:3])

    out = {
        "cid": cid,
        "canonical_name": canonical_name,
        "short_description": short_description,
        "mechanism_summary": mechanism_summary,
        "target_summary": target_summary,
        "safety_summary": safety_summary,
        "props": {
            "formula": props.get("formula"),
            "mw": props.get("mw")
        }
    }
    return out
