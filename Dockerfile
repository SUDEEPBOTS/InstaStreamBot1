# Python 3.10 Base Image
FROM python:3.10-slim

# 1. System Tools aur FFmpeg Libraries install karo
# Ye wo libraries hain jo pichli baar missing thi
RUN apt-get update && apt-get install -y \
    git \
    ffmpeg \
    build-essential \
    python3-dev \
    libavformat-dev \
    libavcodec-dev \
    libavdevice-dev \
    libavutil-dev \
    libswscale-dev \
    libswresample-dev \
    libavfilter-dev \
    pkg-config \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# 2. Working Directory set karo
WORKDIR /app

# 3. Pip Update karo
RUN pip install --upgrade pip setuptools wheel

# 4. Requirements Install karo
COPY requirements.txt .
RUN pip install -r requirements.txt

# 5. 'av' aur 'pytgcalls' ko manually install karo
# Ab hamare paas system libraries hain, toh ye aaram se install ho jayenge
RUN pip install av==10.0.0
RUN pip install --no-deps pytgcalls==3.0.0.dev18

# 6. Baaki Code Copy karo
COPY . .

# 7. Bot Start Command
CMD ["python", "main.py"]
