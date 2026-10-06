PYTHON ?= python

.PHONY: install-tools install-classical install-rag lint validate-artifacts test test-classical test-rag check rag-calibrate rag-eval

install-tools:
	$(PYTHON) -m pip install -r requirements-dev.txt

install-classical:
	$(PYTHON) -m pip install 		-r bank-transaction-fraud-detection/requirements.txt 		-r credit-repayment-prediction/requirements.txt 		-r spam-detector/requirements-dev.txt 		-r T9-typo-correction/requirements.txt

install-rag:
	$(PYTHON) -m pip install -r llm-knowledge-base-assistant/requirements-dev.txt

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

rag-calibrate:
	cd llm-knowledge-base-assistant && PYTHONPATH=. $(PYTHON) eval/calibrate_abstention.py

rag-eval:
	cd llm-knowledge-base-assistant && PYTHONPATH=. $(PYTHON) eval/evaluate_retrieval.py

check: lint validate-artifacts
	$(PYTHON) -m compileall -q 		bank-transaction-fraud-detection 		credit-repayment-prediction 		spam-detector 		T9-typo-correction 		llm-knowledge-base-assistant/app 		llm-knowledge-base-assistant/eval
	$(MAKE) test
