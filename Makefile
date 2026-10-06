PYTHON ?= python

.PHONY: help install-tools install-classical install-rag-test install-rag install-check 	lint validate-artifacts test test-classical test-rag check 	rag-index rag-eval rag-calibrate rag-verify audit

help:
	@echo "Portfolio commands:"
	@echo "  make install-check   Install dependencies required by make check"
	@echo "  make check           Run lint, artifact validation, compile checks and tests"
	@echo "  make audit           Audit pinned project dependencies for known vulnerabilities"
	@echo "  make install-rag     Install the full RAG runtime"
	@echo "  make rag-verify      Rebuild and verify committed RAG evaluation metrics"

install-tools:
	$(PYTHON) -m pip install -r requirements-dev.txt

install-classical:
	$(PYTHON) -m pip install 		-r bank-transaction-fraud-detection/requirements.txt 		-r credit-repayment-prediction/requirements.txt 		-r spam-detector/requirements-dev.txt 		-r T9-typo-correction/requirements.txt

install-rag-test:
	$(PYTHON) -m pip install -r llm-knowledge-base-assistant/requirements-test.txt

install-rag:
	$(PYTHON) -m pip install -r llm-knowledge-base-assistant/requirements-dev.txt

install-check: install-tools install-classical install-rag-test

lint:
	$(PYTHON) -m ruff check .

validate-artifacts:
	$(PYTHON) scripts/validate_results.py

test: test-classical test-rag

test-classical:
	$(PYTHON) -m pytest -q bank-transaction-fraud-detection/tests
	$(PYTHON) -m pytest -q credit-repayment-prediction/tests
	$(PYTHON) -m pytest -q spam-detector/tests
	$(PYTHON) -m pytest -q T9-typo-correction/tests

test-rag:
	cd llm-knowledge-base-assistant && $(PYTHON) -m pytest -q tests

check: lint validate-artifacts
	$(PYTHON) -m compileall -q 		bank-transaction-fraud-detection 		credit-repayment-prediction 		spam-detector 		T9-typo-correction 		llm-knowledge-base-assistant/app 		llm-knowledge-base-assistant/eval
	$(MAKE) test

rag-index:
	cd llm-knowledge-base-assistant && $(PYTHON) -m app.build_index

rag-eval: rag-index
	cd llm-knowledge-base-assistant && PYTHONPATH=. $(PYTHON) eval/evaluate_retrieval.py

rag-calibrate: rag-index
	cd llm-knowledge-base-assistant && PYTHONPATH=. $(PYTHON) eval/calibrate_abstention.py

rag-verify: rag-index
	cd llm-knowledge-base-assistant && PYTHONPATH=. $(PYTHON) eval/evaluate_retrieval.py
	cd llm-knowledge-base-assistant && PYTHONPATH=. $(PYTHON) eval/calibrate_abstention.py
	cd llm-knowledge-base-assistant && PYTHONPATH=. $(PYTHON) eval/verify_snapshot.py

audit:
	cd bank-transaction-fraud-detection && $(PYTHON) -m pip_audit -r requirements.txt
	cd credit-repayment-prediction && $(PYTHON) -m pip_audit -r requirements.txt
	cd spam-detector && $(PYTHON) -m pip_audit -r requirements-dev.txt
	cd T9-typo-correction && $(PYTHON) -m pip_audit -r requirements.txt
	cd llm-knowledge-base-assistant && $(PYTHON) -m pip_audit -r requirements-dev.txt
