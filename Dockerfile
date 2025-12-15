FROM python:3.10-slim

# ---------- SYSTEM DEPS ----------
RUN apt-get update && apt-get install -y \
    ffmpeg \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

# ---------- PYTHON ----------
RUN pip install --upgrade pip setuptools wheel

# Project deps (NO av here)
RUN pip install -r requirements.txt

# VC deps (binary wheels available)
RUN pip install av==12.0.0 pytgcalls==3.0.0.dev18

CMD ["python", "main.py"]
