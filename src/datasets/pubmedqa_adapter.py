import json, re
from typing import List, Dict, Any

from .base_adapter import DatasetAdapter

class PubMedQAAdapter(DatasetAdapter):
    """
    Expects a JSON or JSONL file with fields like: question, abstract/context, final_decision (yes/no/maybe)
    """

    def load_records(self, raw_path: str) -> List[Dict[str, Any]]:
        rows = []
        with open(raw_path, "r", encoding="utf-8") as f:
            head = f.read(1); f.seek(0)
            if head == "[":
                rows = json.load(f)
            else:
                for line in f:
                    if line.strip():
                        rows.append(json.loads(line))
        return rows

    def _norm(self, rec: Dict[str, Any]):
        q = rec.get("question") or rec.get("QUESTION") or ""
        ctx = rec.get("context") or rec.get("abstract") or rec.get("CONTEXT") or ""
        y = (rec.get("final_decision") or rec.get("answer") or rec.get("LABEL") or "").lower()
        q = re.sub(r"\s+", " ", q).strip()
        ctx = re.sub(r"\s+", " ", ctx).strip()
        y = y.strip()
        return q, ctx, y

    def to_examples(self, records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        out = []
        for rec in records:
            q, ctx, y = self._norm(rec)
            if not q or not ctx or y not in {"yes", "no", "maybe"}:
                continue
            user_block = (
                "You are given a biomedical research question and an abstract.\n"
                "Answer strictly in this format:\n"
                "1) Final: <yes|no|maybe>\n"
                "2) Evidence:\n- <bullet 1>\n- <bullet 2>\n\n"
                f"Question: {q}\nAbstract: {ctx}\n"
            )
            out.append({
                "input": user_block,
                "reference": y,
                "meta": {"dataset": "pubmedqa", "label": y}
            })
        return out
