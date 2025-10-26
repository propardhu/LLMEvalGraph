import re

def extract_label(output: str) -> str:
    if not output:
        return ""
    m = re.search(r"final:\s*(yes|no|maybe)", output, flags=re.I)
    return m.group(1).lower() if m else ""

def accuracy(output: str, reference: str) -> float:
    return 1.0 if extract_label(output) == (reference or "").strip().lower() else 0.0

def structure(output: str) -> float:
    s = (output or "").lower()
    sc = 0.0
    if "final:" in s: sc += 0.5
    if "evidence:" in s: sc += 0.5
    return sc

def citation_rate(output: str) -> float:
    s = (output or "").lower()
    return 1.0 if ("http://" in s or "https://" in s) else 0.0
