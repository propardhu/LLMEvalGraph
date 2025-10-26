# 🧠 LLMEvalGraph

**LLMEvalGraph** is a **modular evaluation framework** built using  
**LangChain**, **LangGraph**, and **LangSmith** — designed to benchmark and compare Large Language Models (LLMs) across any dataset or domain.

It provides a **structured, reproducible pipeline** for:
- Comparing base and fine-tuned models (e.g., GPT-4o-mini vs Mistral-7B)
- Evaluating on any public or custom dataset (e.g., PubMedQA, LegalBench, FinanceQA)
- Logging, tracing, and analyzing every step through LangSmith
- Defining consistent metrics (accuracy, structure, latency, etc.)
- Visualizing and exporting results for research or production monitoring

---

## ⚙️ Features

✅ **Model-agnostic** – swap any model or provider (OpenAI, Mistral, Anthropic, etc.)  
✅ **Dataset-agnostic** – plug in any JSONL dataset with `input` + `reference` fields  
✅ **LangGraph Orchestration** – manage nodes, retries, validation, and state  
✅ **LangSmith Observability** – trace every run, compare versions, run evaluations  
✅ **Fully reproducible** – consistent Makefile + environment setup for experiments  

---

## 🧩 Project structure

Below is the repository layout. Put datasets under `data/raw/` and expect processed JSONL splits to appear in `data/processed/`.

```
LLMEvalGraph/
├─ data/
│  ├─ raw/           # put your dataset here
│  └─ processed/     # generated dev/test JSONL splits
├─ src/
│  ├─ prep_dataset.py  # convert your dataset to JSONL
│  ├─ prompts.py       # prompt templates
│  ├─ runnables.py     # LangChain model wrappers
│  ├─ graph.py         # LangGraph orchestration
│  ├─ evaluators.py    # metrics (accuracy, structure, etc.)
│  ├─ run_eval.py      # main runner
│  └─ utils.py         # helpers (IO, timing)
├─ results/            # output JSONs with metrics
├─ requirements.txt
├─ Makefile
└─ README.md
```


