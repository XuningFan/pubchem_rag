
import requests
from typing import Dict, Any, List, Optional

BASE_REST = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"
BASE_VIEW = "https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound"

def _safe_get(d: dict, *path, default=None):
    cur = d
    for p in path:
        if isinstance(cur, dict) and p in cur:
            cur = cur[p]
        else:
            return default
    return cur

def _extract_string_list_from_InfoBlock(info_block: dict) -> List[str]:
    out = []
    val = info_block.get("Value", {})
    swm = val.get("StringWithMarkup", [])
    for item in swm:
        s = item.get("String")
        if s:
            out.append(s.strip())
    return out

def _walk_sections(sections: List[dict], bucket: Dict[str, Any]):
    if not sections:
        return
    for sec in sections:
        heading = sec.get("TOCHeading", "") or ""
        lower_head = heading.lower()

        info_list = sec.get("Information", []) or []
        collected_texts = []
        for info in info_list:
            collected_texts.extend(_extract_string_list_from_InfoBlock(info))

        if any(k in lower_head for k in ["pharmacology", "pharmacodynamics", "pharmacology and biochemistry", "drug indications"]):
            bucket["pharmacology_texts"].extend(collected_texts)

        if "mechanism of action" in lower_head:
            bucket["mechanism_texts"].extend(collected_texts)

        if "target" in lower_head or "targets" in lower_head or "drug target" in lower_head:
            for t in collected_texts:
                for piece in t.split("\n"):
                    piece = piece.strip()
                    if piece and len(piece) < 200:
                        bucket["target_names"].append(piece)

        if ("toxicity" in lower_head) or ("toxicological" in lower_head) or ("health hazard" in lower_head):
            bucket["tox_texts"].extend(collected_texts)

        if ("safety" in lower_head) or ("hazard" in lower_head) or ("ghs" in lower_head):
            bucket["hazard_texts"].extend(collected_texts)

        _walk_sections(sec.get("Section", []) or [], bucket)

def _fetch_synonyms(cid: int) -> Dict[str, Any]:
    url = f"{BASE_REST}/compound/cid/{cid}/synonyms/JSON"
    out_names = {
        "canonical": None,
        "synonyms": []
    }
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            js = r.json()
            info = _safe_get(js, "InformationList", "Information", default=[])
            if info and isinstance(info, list):
                syns = info[0].get("Synonym", []) or []
                out_names["synonyms"] = syns
                if syns:
                    out_names["canonical"] = syns[0]
    except Exception:
        pass
    return out_names

def _fetch_properties(cid: int) -> Dict[str, Any]:
    prop_url = (
        f"{BASE_REST}/compound/cid/{cid}/property/"
        "MolecularFormula,MolecularWeight,CanonicalSMILES/JSON"
    )
    props_out = {
        "formula": None,
        "mw": None,
        "smiles": None
    }
    try:
        r = requests.get(prop_url, timeout=10)
        if r.status_code == 200:
            js = r.json()
            props_list = _safe_get(js, "PropertyTable", "Properties", default=[])
            if props_list and isinstance(props_list, list):
                p0 = props_list[0]
                if "MolecularFormula" in p0:
                    props_out["formula"] = p0["MolecularFormula"]
                if "MolecularWeight" in p0:
                    try:
                        props_out["mw"] = float(p0["MolecularWeight"])
                    except Exception:
                        props_out["mw"] = p0["MolecularWeight"]
                if "CanonicalSMILES" in p0:
                    props_out["smiles"] = p0["CanonicalSMILES"]
    except Exception:
        pass
    return props_out

def _fetch_view_annotations(cid: int) -> Dict[str, Any]:
    url = f"{BASE_VIEW}/{cid}/JSON"
    bucket = {
        "pharmacology_texts": [],
        "mechanism_texts": [],
        "target_names": [],
        "tox_texts": [],
        "hazard_texts": []
    }

    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            js = r.json()
            sections = _safe_get(js, "Record", "Section", default=[])
            _walk_sections(sections, bucket)
    except Exception:
        pass

    pharmacology = " ".join(bucket["pharmacology_texts"]).strip() or None
    mechanism = " ".join(bucket["mechanism_texts"]).strip() or None
    tox_summary = " ".join(bucket["tox_texts"]).strip() or None

    hazard_statements = [h.strip() for h in bucket["hazard_texts"] if h.strip()]
    seen_h = set()
    hazard_final = []
    for h in hazard_statements:
        if h not in seen_h:
            hazard_final.append(h)
            seen_h.add(h)

    seen_t = set()
    targets_final = []
    for t in bucket["target_names"]:
        t_clean = t.strip()
        if not t_clean:
            continue
        if len(t_clean) > 200:
            continue
        low = t_clean.lower()
        if low not in seen_t:
            seen_t.add(low)
            targets_final.append(t_clean)

    return {
        "pharmacology": pharmacology,
        "mechanism": mechanism,
        "targets": targets_final,
        "safety": {
            "hazard_statements": hazard_final,
            "toxicology_summary": tox_summary
        }
    }

def fetch_compound_info_by_cid(cid: int) -> Dict[str, Any]:
    names = _fetch_synonyms(cid)
    props = _fetch_properties(cid)
    ann   = _fetch_view_annotations(cid)

    out = {
        "cid": cid,
        "names": names,
        "properties": props,
        "pharmacology": ann.get("pharmacology"),
        "mechanism": ann.get("mechanism"),
        "targets": ann.get("targets", []),
        "safety": ann.get("safety", {
            "hazard_statements": [],
            "toxicology_summary": None
        })
    }
    return out

def fetch_compound_info_by_name(term: str) -> Optional[Dict[str, Any]]:
    # TODO: resolve name -> CID via:
    # GET {BASE_REST}/compound/name/<term>/cids/JSON
    # then call fetch_compound_info_by_cid on first CID.
    return None
