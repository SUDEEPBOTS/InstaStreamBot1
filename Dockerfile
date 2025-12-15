FROM python:3.10-slim

# System deps
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

RUN pip install --upgrade pip setuptools wheel

# Project deps
RUN pip install -r requirements.txt

# VC streaming (STABLE)
RUN pip install pytgcalls==1.2.0

CMD ["python", "main.py"]
