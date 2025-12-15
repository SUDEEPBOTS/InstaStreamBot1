FROM python:3.10-slim

# ---------- SYSTEM DEPENDENCIES ----------
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libavformat-dev \
    libavcodec-dev \
    libavdevice-dev \
    libavutil-dev \
    libavfilter-dev \
    libswscale-dev \
    libswresample-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# ---------- WORKDIR ----------
WORKDIR /app
COPY . .

# ---------- PYTHON DEPENDENCIES ----------
RUN pip install --upgrade pip setuptools wheel
# PyAV bug fix for Python 3.10
RUN pip install "cython<3"
# Install project requirements
RUN pip install -r requirements.txt
# Install av and pytgcalls for VC streaming
RUN pip install av==10.0.0 pytgcalls==3.0.0.dev18

# ---------- RUN BOT ----------
CMD ["python", "main.py"]
