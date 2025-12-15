FROM python:3.10-slim

RUN apt-get update && apt-get install -y ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

RUN pip install --upgrade pip setuptools wheel

# 🔥 HARD BLOCK SOURCE BUILDS
ENV PIP_ONLY_BINARY=:all:

RUN pip install av>=12.0.0
RUN pip install -r requirements.txt

CMD ["python", "main.py"]
