# ====== CONFIG ======
PY ?= python

# Raw data & processed outputs
RAW ?= data/raw/ori_pqal.json
TEST_MAP ?= data/raw/test_ground_truth.json
DEV_OUT ?= data/processed/dev.jsonl
TEST_OUT ?= data/processed/test.jsonl

# Split sizes (used when not pinning a test set)
DEV_SIZE ?= 200
TEST_SIZE ?= 200

# Models (override at call time if you want)
OPENAI_MODEL ?= gpt-4o-mini
MISTRAL_MODEL ?= mistral-7b

# ====== ENV ======
env:
	cp -n .env.example .env || true

# ====== DATA PREP ======
# A) Random split (no fixed test set)
prep-pubmedqa:
	$(PY) src/prep_dataset.py --dataset pubmedqa \
		--raw $(RAW) \
		--dev_out $(DEV_OUT) \
		--test_out $(TEST_OUT) \
		--dev_size $(DEV_SIZE) \
		--test_size $(TEST_SIZE)

# B) Fixed test split using a PMID -> label map (recommended)
prep-pubmedqa-fixedtest:
	$(PY) src/prep_dataset.py --dataset pubmedqa \
		--raw $(RAW) \
		--test_label_map $(TEST_MAP) \
		--dev_out $(DEV_OUT) \
		--test_out $(TEST_OUT) \
		--dev_size $(DEV_SIZE)

# ====== DEV RUNS ======
dev-openai:
	$(PY) src/run_eval.py --path $(DEV_OUT) --variant openai --model $(OPENAI_MODEL) --out results/dev_openai.json

dev-mistral:
	$(PY) src/run_eval.py --path $(DEV_OUT) --variant mistral --model $(MISTRAL_MODEL) --out results/dev_mistral.json

# ====== TEST RUNS ======
test-openai:
	$(PY) src/run_eval.py --path $(TEST_OUT) --variant openai --model $(OPENAI_MODEL) --out results/test_openai.json

test-mistral:
	$(PY) src/run_eval.py --path $(TEST_OUT) --variant mistral --model $(MISTRAL_MODEL) --out results/test_mistral.json

compare:
	$(PY) src/compare_results.py --pattern "results/*.json" --out_csv results/summary.csv --out_md results/summary.md

# ====== QUICK SMOKE (small dev split) ======
# Example: make prep-smoke DEV_SIZE=50
prep-smoke:
	$(PY) src/prep_dataset.py --dataset pubmedqa \
		--raw $(RAW) \
		--dev_out $(DEV_OUT) \
		--test_out $(TEST_OUT) \
		--dev_size $(DEV_SIZE) \
		--test_size 0

smoke:
	$(MAKE) dev-openai
	$(MAKE) dev-mistral

# ====== FULL RUNS ======
# Random split path:
full-random: prep-pubmedqa dev-openai dev-mistral test-openai test-mistral

# Fixed test path (uses TEST_MAP):
full-fixed: prep-pubmedqa-fixedtest dev-openai dev-mistral test-openai test-mistral

.PHONY: env prep-pubmedqa prep-pubmedqa-fixedtest dev-openai dev-mistral test-openai test-mistral prep-smoke smoke full-random full-fixed
