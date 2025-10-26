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

```
LLMEvalGraph/
├─ data/
│  ├─ raw/           # put your dataset here
│  └─ processed/     # generated dev/test JSONL splits
├─ src/
│  ├─ prep_dataset.py   # convert raw data into processed splits
│  ├─ run_eval.py       # main entry for evaluation
│  ├─ runnables.py      # model wrappers (OpenAI, Mistral, etc.)
│  ├─ graph.py          # LangGraph orchestration logic
│  ├─ evaluators.py     # metric calculations
│  ├─ compare_results.py# merges results into markdown/csv
│  └─ utils.py          # helper functions
├─ results/             # output JSONs and summary tables
├─ requirements.txt
├─ Makefile
└─ README.md
```

---

## 🚀 Quickstart

```bash
git clone https://github.com/propardhu/LLMEvalGraph
cd LLMEvalGraph

# create virtual environment
python -m venv .venv
source .venv/bin/activate   # (Windows: .venv\Scripts\activate)

# install dependencies
pip install -r requirements.txt

# setup environment
cp .env.example .env
```

Open `.env` and paste your API keys:
```
OPENAI_API_KEY=sk-...
MISTRAL_API_KEY=app-...
LANGSMITH_API_KEY=lsm-...
LANGSMITH_TRACING=true
LANGSMITH_PROJECT=llm-evalgraph
```

---

## 📦 Prepare your dataset

Place your raw PubMedQA files:
```
data/raw/ori_pqal.json
data/raw/test_ground_truth.json   # optional (for fixed test set)
```

Then run **one** of the following:

**A) Fixed test (recommended):**
```bash
make prep-pubmedqa-fixedtest
```

**B) Random split:**
```bash
make prep-pubmedqa
```

You’ll get:
```
data/processed/dev.jsonl
data/processed/test.jsonl
```

---

## 🤖 Run evaluations

**Development runs (small split for testing):**
```bash
make dev-openai
make dev-mistral
```

**Full test runs:**
```bash
make test-openai
make test-mistral
```

Results will be saved in:
```
results/dev_openai.json
results/dev_mistral.json
results/test_openai.json
results/test_mistral.json
```

---

## 📊 Compare and summarize

Combine all metrics into one table:
```bash
make compare
```

This generates:
```
results/summary.md
results/summary.csv
```

The Markdown version can be directly pasted into your Medium article or documentation.

---

## 🔁 Changing models easily

Default models are defined in the Makefile:
```
OPENAI_MODEL ?= gpt-4o-mini
MISTRAL_MODEL ?= open-mistral-7b
```

You can override them at runtime:
```bash
make dev-mistral MISTRAL_MODEL=mistral-small-latest
make dev-openai  OPENAI_MODEL=gpt-4o-mini
```

> ⚠️ If you see `Invalid model: mistral-7b`, use `open-mistral-7b` or one of the hosted versions like `mistral-small-latest`.

---

## 🧪 Metric definitions

| Metric | Description |
|---------|--------------|
| **accuracy** | % of answers matching the gold label (yes/no/maybe) |
| **structure** | % of responses following the required output format |
| **citation_rate** | % of outputs containing URLs or references |
| **latency_s_per_item** | Average time (in seconds) to generate each answer |

---

## 🧰 Troubleshooting

| Problem | Fix |
|----------|-----|
| Empty `dev/test.jsonl` | Ensure your raw dataset is a JSON dict with PMIDs and `CONTEXTS` fields |
| `Invalid model` error | Use `open-mistral-7b` instead of `mistral-7b` |
| Authentication error | Double-check your `.env` keys |
| Windows “make not found” | Use WSL (`sudo apt install make`) or run commands manually |

---

## 🧱 Extending LLMEvalGraph

- **New dataset:** add a file like `my_dataset_adapter.py` in `src/datasets/`  
- **New model:** register it in `src/runnables.py` and the Makefile  
- **New metrics:** define in `src/evaluators.py` and include in the comparison step  

---

## 🌐 Repository

🔗 **GitHub:** [https://github.com/propardhu/LLMEvalGraph](https://github.com/propardhu/LLMEvalGraph)

---

**LLMEvalGraph** aims to make LLM benchmarking simple, consistent, and transparent —  
so you can focus on insights, not setup.
