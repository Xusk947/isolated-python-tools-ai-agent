FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    MPLBACKEND=Agg

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY server.py /app/server.py
COPY sandbox_client.py /app/sandbox_client.py
COPY artifact_hooks.py /app/artifact_hooks.py

WORKDIR /workspace
CMD ["python3", "/app/server.py"]

