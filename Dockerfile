FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

RUN pip install --upgrade pip setuptools wheel

# 🔥 MOST IMPORTANT LINE (AV FIX)
RUN pip install --only-binary=:all: "av>=12.0.0"

RUN pip install -r requirements.txt

# VC (stable)
RUN pip install py-tgcalls==0.9.7

CMD ["python", "main.py"]
