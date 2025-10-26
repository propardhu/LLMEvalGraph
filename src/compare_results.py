import json, os, glob
import argparse
from typing import Dict, Any, List

METRICS = ["accuracy", "structure", "citation_rate", "latency_s_per_item"]

def infer_split_and_variant(path: str):
    name = os.path.basename(path).replace(".json", "")
    # expected: dev_openai, dev_mistral, test_openai, test_mistral
    bits = name.split("_", 1)
    split = bits[0] if bits else "unknown"
    variant = bits[1] if len(bits) > 1 else "unknown"
    return split, variant

def load_result(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    split, variant = infer_split_and_variant(path)
    row = {
        "file": os.path.basename(path),
        "split": split,
        "variant": data.get("variant", variant),
        "model_id": data.get("model_id", ""),
        "count": data.get("count", ""),
    }
    for m in METRICS:
        row[m] = data.get(m, "")
    return row

def fmt_num(x):
    if isinstance(x, (int,)) and not isinstance(x, bool):
        return str(x)
    try:
        return f"{float(x):.3f}"
    except Exception:
        return str(x)

def to_markdown(rows: List[Dict[str, Any]]) -> str:
    headers = ["split", "variant", "model_id", "count"] + METRICS
    md = []
    md.append("| " + " | ".join(headers) + " |")
    md.append("|" + "|".join(["---"] * len(headers)) + "|")
    for r in rows:
        md.append("| " + " | ".join(fmt_num(r.get(h, "")) for h in headers) + " |")
    return "\n".join(md)

def to_csv(rows: List[Dict[str, Any]]) -> str:
    headers = ["split", "variant", "model_id", "count"] + METRICS
    lines = [",".join(headers)]
    for r in rows:
        vals = [str(r.get(h, "")) if h in ("split","variant","model_id")
                else fmt_num(r.get(h, "")) for h in headers]
        # rudimentary CSV escaping
        vals = [v.replace(",", ";") for v in vals]
        lines.append(",".join(vals))
    return "\n".join(lines)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pattern", default="results/*.json", help="glob pattern for result JSONs")
    ap.add_argument("--out_csv", default="results/summary.csv")
    ap.add_argument("--out_md", default="results/summary.md")
    args = ap.parse_args()

    files = sorted(glob.glob(args.pattern))
    if not files:
        print(f"No files matched {args.pattern}")
        return

    rows = [load_result(p) for p in files]

    # Pretty print to console
    print("\n== Combined Results ==\n")
    print(to_markdown(rows))
    print("\nSaved:")
    os.makedirs(os.path.dirname(args.out_csv), exist_ok=True)
    with open(args.out_csv, "w", encoding="utf-8") as f:
        f.write(to_csv(rows))
    with open(args.out_md, "w", encoding="utf-8") as f:
        f.write(to_markdown(rows))
    print(f" - {args.out_csv}")
    print(f" - {args.out_md}")

if __name__ == "__main__":
    main()
