import json, time
from typing import Any, Dict, List

def read_jsonl(path: str) -> List[Dict[str, Any]]:
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))
    return rows

def write_json(obj: Dict[str, Any], path: str):
    import os
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)

class Timer:
    def __enter__(self):
        self.t0 = time.time()
        return self
    def __exit__(self, *exc):
        self.dt = time.time() - self.t0
