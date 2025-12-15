FROM python:3.10-slim

# ---------- SYSTEM DEPENDENCIES ----------
RUN apt-get update && apt-get install -y \
    ffmpeg \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# ---------- WORKDIR ----------
WORKDIR /app
COPY . .

# ---------- PYTHON SETUP ----------
ENV PIP_ONLY_BINARY=av
ENV PIP_NO_BUILD_ISOLATION=1

RUN pip install --upgrade pip setuptools wheel
RUN pip install cython==0.29.36

# Install project deps FIRST (without av inside)
RUN pip install -r requirements.txt

# Install PyAV + PyTgCalls from wheels only
RUN pip install av==10.0.0 pytgcalls==3.0.0.dev18

# ---------- RUN ----------
CMD ["python", "main.py"]
