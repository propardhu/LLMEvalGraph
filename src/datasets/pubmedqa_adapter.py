import json
import re
from typing import List, Dict, Any, Tuple, Optional

from .base_adapter import DatasetAdapter

def _join_contexts(ctx: Any) -> str:
    """Join a list of strings or pass through a string."""
    if isinstance(ctx, list):
        return " ".join(s for s in ctx if isinstance(s, str))
    if isinstance(ctx, str):
        return ctx
    return ""

def _lower(x: Optional[str]) -> str:
    return (x or "").strip().lower()

class PubMedQAAdapter(DatasetAdapter):
    """
    Supports PubMedQA variants:
      - Dict-root JSON: { "<PMID>": { QUESTION, CONTEXTS, final_decision, ... }, ... }
      - JSON array: [ {...}, {...} ]
      - JSONL: one JSON object per line
    Normalizes each record to {"input", "reference", "meta"} where:
      - input: formatted prompt block with Question + Abstract
      - reference: "yes" | "no" | "maybe"
      - meta: {"dataset":"pubmedqa","label":..., "pmid": "<id>" (if available)}
    """

    # ---------- LOADING ----------
    def load_records(self, raw_path: str) -> List[Dict[str, Any]]:
        with open(raw_path, "r", encoding="utf-8") as f:
            text = f.read()
        s = text.lstrip()
        if not s:
            return []

        # JSON array
        if s.startswith("["):
            return json.loads(text)

        # Try JSON object (dict-root)
        try:
            obj = json.loads(text)
            if isinstance(obj, dict):
                out = []
                for pmid, rec in obj.items():
                    if isinstance(rec, dict):
                        rec = dict(rec)
                        rec["PMID"] = str(pmid)
                        out.append(rec)
                if out:
                    return out
        except json.JSONDecodeError:
            pass

        # Fallback: JSONL (one object per line)
        rows: List[Dict[str, Any]] = []
        for line in text.splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                # Skip malformed lines
                continue
        return rows

    # ---------- NORMALIZATION ----------
    def _norm(self, rec: Dict[str, Any]) -> Tuple[str, str, str, str]:
        """
        Return (question, abstract, label, pmid)
        Accepts multiple field name variants.
        """
        # Question
        q = rec.get("question") or rec.get("QUESTION") or ""

        # Context / Abstract — support "context", "CONTEXT", and **CONTEXTS (list)**
        ctx = (
            rec.get("context")
            or rec.get("CONTEXT")
            or rec.get("abstract")
            or rec.get("ABSTRACT")
            or _join_contexts(rec.get("CONTEXTS"))  # <- PubMedQA commonly uses this
        )

        # Label
        y = (
            rec.get("final_decision")
            or rec.get("answer")
            or rec.get("LABEL")
            or ""
        )

        # PMID (if available)
        pmid = str(rec.get("PMID") or rec.get("pmid") or "").strip()

        # Cleanup
        q = re.sub(r"\s+", " ", q or "").strip()
        ctx = re.sub(r"\s+", " ", (ctx or "")).strip()
        y = _lower(str(y))

        return q, ctx, y, pmid

    # ---------- EXAMPLES ----------
    def to_examples(self, records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        out: List[Dict[str, Any]] = []
        for rec in records:
            q, ctx, y, pmid = self._norm(rec)
            if not q or not ctx:
                continue
            if y not in {"yes", "no", "maybe"}:
                continue

            user_block = (
                "You are given a biomedical research question and an abstract.\n"
                "Answer strictly in this format:\n"
                "1) Final: <yes|no|maybe>\n"
                "2) Evidence:\n- <bullet 1>\n- <bullet 2>\n\n"
                f"Question: {q}\nAbstract: {ctx}\n"
            )

            meta = {"dataset": "pubmedqa", "label": y}
            if pmid:
                meta["pmid"] = pmid

            out.append({
                "input": user_block,
                "reference": y,
                "meta": meta,
            })
        return out
