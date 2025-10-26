import argparse, random, os, json
from typing import List, Dict, Any
from pathlib import Path

from datasets.pubmedqa_adapter import PubMedQAAdapter

ADAPTERS = {
    "pubmedqa": PubMedQAAdapter,
}

def write_jsonl(rows: List[Dict[str, Any]], path: str) -> int:
    os.makedirs(Path(path).parent, exist_ok=True)
    n = 0
    with open(path, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
            n += 1
    return n

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", required=True, choices=ADAPTERS.keys())
    ap.add_argument("--raw", required=True, help="path to raw dataset file (JSON or JSONL)")
    ap.add_argument("--dev_out", default="data/processed/dev.jsonl")
    ap.add_argument("--test_out", default="data/processed/test.jsonl")
    ap.add_argument("--dev_size", type=int, default=200)
    ap.add_argument("--test_size", type=int, default=200)
    args = ap.parse_args()

    adapter = ADAPTERS[args.dataset]()  # type: ignore
    records = adapter.load_records(args.raw)

    random.seed(42)
    random.shuffle(records)

    dev_raw = records[:args.dev_size]
    test_raw = records[args.dev_size : args.dev_size + args.test_size]

    dev = adapter.to_examples(dev_raw)
    test = adapter.to_examples(test_raw)

    n_dev = write_jsonl(dev, args.dev_out)
    n_test = write_jsonl(test, args.test_out)

    print(f"Wrote dev={n_dev} → {args.dev_out}")
    print(f"Wrote test={n_test} → {args.test_out}")

if __name__ == "__main__":
    main()
