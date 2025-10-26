PY=python

env:
	cp -n .env.example .env || true

# ==== DATA PREP ====
# Example: PubMedQA adapter expects a single JSON/JSONL at data/raw/pubmedqa.json
prep-pubmedqa:
	$(PY) src/prep_dataset.py --dataset pubmedqa \
		--raw data/raw/pubmedqa.json \
		--dev_out data/processed/dev.jsonl \
		--test_out data/processed/test.jsonl \
		--dev_size 200 --test_size 200

# ==== DEV RUNS ====
dev-openai:
	$(PY) src/run_eval.py --path data/processed/dev.jsonl --variant openai --out results/dev_openai.json

dev-mistral:
	$(PY) src/run_eval.py --path data/processed/dev.jsonl --variant mistral --out results/dev_mistral.json

# ==== TEST RUNS ====
test-openai:
	$(PY) src/run_eval.py --path data/processed/test.jsonl --variant openai --out results/test_openai.json

test-mistral:
	$(PY) src/run_eval.py --path data/processed/test.jsonl --variant mistral --out results/test_mistral.json
# ==== FULL RUNS ====