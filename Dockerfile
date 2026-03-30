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
    && fc-cache -f \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

RUN mkdir -p /usr/local/share/fonts/unbounded \
    && curl -fsSL "https://raw.githubusercontent.com/w3f/unbounded/b32de1cba1743ccdba717843a048f79376044911/TTF/Unbounded-Regular.ttf" -o /usr/local/share/fonts/unbounded/Unbounded-Regular.ttf \
    && fc-cache -f

RUN mkdir -p /app/mplconfig && python3 -c "import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt; plt.figure(); plt.plot([0,1],[0,1]); plt.savefig('/tmp/_croki_mpl_warm.png');"

COPY server.py /app/server.py
COPY sandbox_client.py /app/sandbox_client.py
COPY artifact_hooks.py /app/artifact_hooks.py
COPY theme.py /app/theme.py

WORKDIR /workspace
CMD ["python3", "/app/server.py"]
