FROM python:3.10-slim

# System deps
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

RUN pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt

# VC streaming (REAL stable version)
RUN pip install pytgcalls==0.9.7

CMD ["python", "main.py"]
