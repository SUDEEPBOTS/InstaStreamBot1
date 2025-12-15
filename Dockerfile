FROM python:3.10-slim

# System dependencies - ab build tools bhi add karo
RUN apt-get update && apt-get install -y \
    ffmpeg \
    pkg-config \
    python3-dev \
    gcc \
    g++ \
    make \
    libavformat-dev \
    libavcodec-dev \
    libavdevice-dev \
    libavutil-dev \
    libavfilter-dev \
    libswscale-dev \
    libswresample-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

RUN pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt

# Voice Chat streaming
RUN pip install pytgcalls==3.0.0.dev24

CMD ["python", "main.py"]
