FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/workspace/apps/api

WORKDIR /workspace

COPY apps/api/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY apps/api ./apps/api
COPY bank-transaction-fraud-detection ./bank-transaction-fraud-detection
COPY credit-repayment-prediction ./credit-repayment-prediction
COPY spam-detector ./spam-detector
COPY T9-typo-correction ./T9-typo-correction
COPY llm-knowledge-base-assistant/eval ./llm-knowledge-base-assistant/eval

USER 10001:10001

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=3)"

CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
