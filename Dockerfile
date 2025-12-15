
FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    ffmpeg \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

RUN pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt

# VC streaming deps (WORKING)
RUN pip install av==12.0.0 pytgcalls==3.0.0.dev6

CMD ["python", "main.py"]
