PYTHON ?= python

.PHONY: install-classical install-rag test test-classical test-rag check

install-classical:
	$(PYTHON) -m pip install 		-r bank-transaction-fraud-detection/requirements.txt 		-r credit-repayment-prediction/requirements.txt 		-r spam-detector/requirements-dev.txt 		-r T9-typo-correction/requirements.txt

install-rag:
	$(PYTHON) -m pip install -r llm-knowledge-base-assistant/requirements-dev.txt

test: test-classical test-rag

test-classical:
	$(PYTHON) -m pytest -q bank-transaction-fraud-detection/tests
	$(PYTHON) -m pytest -q credit-repayment-prediction/tests
	$(PYTHON) -m pytest -q spam-detector/tests
	$(PYTHON) -m pytest -q T9-typo-correction/tests

test-rag:
	$(PYTHON) -m pytest -q llm-knowledge-base-assistant/tests

check:
	$(PYTHON) -m compileall -q 		bank-transaction-fraud-detection 		credit-repayment-prediction 		spam-detector 		T9-typo-correction 		llm-knowledge-base-assistant/app 		llm-knowledge-base-assistant/eval
	$(MAKE) test
