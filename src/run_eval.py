import os, argparse, json
from dotenv import load_dotenv
from utils import read_jsonl, write_json, Timer
from runnables import make_openai, make_mistral
from graph import build_graph
from evaluators import accuracy, structure, citation_rate

def main():
    load_dotenv()

    ap = argparse.ArgumentParser()
    ap.add_argument("--path", default="data/processed/dev.jsonl")
    ap.add_argument("--variant", choices=["openai","mistral"], default="openai")
    ap.add_argument("--model", default=None, help="optional model id override")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    if args.variant == "openai":
        runnable = make_openai(args.model or "gpt-4o-mini", temperature=0.0)
    else:
        runnable = make_mistral(args.model or "mistral-7b", temperature=0.0)

    graph = build_graph(runnable)
    rows = read_jsonl(args.path)

    acc = struct = cite = 0.0
    outputs = []

    with Timer() as t:
        for ex in rows:
            s = {"question_ctx": ex["input"], "draft": "", "flags": []}
            out = graph.invoke(s)
            text = out["draft"]
            ref = ex.get("reference", "")
            acc += accuracy(text, ref)
            struct += structure(text)
            cite += citation_rate(text)
            outputs.append({"input": ex["input"], "output": text, "reference": ref, "flags": out.get("flags", [])})

    n = max(1, len(rows))
    result = {
        "variant": args.variant,
        "model_id": args.model,
        "count": len(rows),
        "latency_s_per_item": t.dt / n,
        "accuracy": acc / n,
        "structure": struct / n,
        "citation_rate": cite / n,
        "preview_samples": outputs[:5]
    }

    print(json.dumps(result, indent=2))
    if args.out:
        write_json(result, args.out)

if __name__ == "__main__":
    main()
