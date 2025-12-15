FROM python:3.10-slim

# System dependencies (safe even if av not used)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

# Python deps
RUN pip install --upgrade pip setuptools wheel
RUN pip install "cython<3"
RUN pip install -r requirements.txt

CMD ["python", "main.py"]
