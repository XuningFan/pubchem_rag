
BANNED_KEYWORDS = [
    "synthesis", "synthesize", "route", "procedure",
    "step-by-step", "protocol", "detailed protocol",
    "dosage optimization", "scale-up", "purify", "extraction",
    "weaponize", "toxic gas", "kill", "poison", "explosive"
]

def needs_strict_safety(user_query: str) -> bool:
    q = user_query.lower()
    for kw in BANNED_KEYWORDS:
        if kw in q:
            return True
    return False

def safety_prefix(strict: bool) -> str:
    if strict:
        return (
            "SAFETY NOTICE:\n"
            "The user request may involve experimental procedures or misuse.\n"
            "You MUST refuse to provide any stepwise experimental protocol, "
            "synthetic route, purification procedure, dosage manipulation guidance, "
            "or instructions that enable harm, weaponization, or illicit use.\n"
            "You may provide only high-level, widely known conceptual summaries, "
            "focusing on general pharmacology, known safety risks, and regulatory concerns.\n\n"
        )
    else:
        return (
            "SAFETY NOTICE:\n"
            "Do not provide laboratory steps, synthesis routes, specific experimental conditions, "
            "scale-up instructions, or guidance that could enable harm. "
            "Keep the discussion high-level, conceptual, and safety-aware.\n\n"
        )
