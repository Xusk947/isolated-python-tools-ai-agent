FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    MPLBACKEND=Agg \
    MPLCONFIGDIR=/app/mplconfig

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    chromium \
    curl \
    fontconfig \
    fonts-dejavu-core \
    fonts-lato \
    fonts-noto-core \
    && fc-cache -f \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy and install local fonts
COPY fonts/ /usr/local/share/fonts/
RUN fc-cache -f

# Pre-generate matplotlib font cache to include new fonts
RUN mkdir -p /app/mplconfig && python3 -c "import matplotlib.font_manager; import os; cache_file = os.path.join('/app/mplconfig', 'fontlist-v390.json'); [os.remove(cache_file) if os.path.exists(cache_file) else None]; matplotlib.font_manager._load_fontmanager(try_read_cache=False); print(f'Matplotlib fonts cached: {len(matplotlib.font_manager.fontManager.ttflist)}')"

COPY server.py /app/server.py
COPY sandbox_client.py /app/sandbox_client.py
COPY artifact_hooks.py /app/artifact_hooks.py
COPY theme.py /app/theme.py

WORKDIR /workspace
CMD ["python3", "/app/server.py"]
