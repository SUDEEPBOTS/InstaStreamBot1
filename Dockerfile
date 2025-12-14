# Hum 'Slim' ki jagah Full version use karenge (RAM bachane ke liye)
FROM python:3.10

WORKDIR /app

# 1. Sirf FFmpeg install karo (Baaki sab is image mein pehle se hai)
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    rm -rf /var/lib/apt/lists/*

# 2. Files copy karo
COPY . .

# 3. Pip update aur Requirements install
RUN pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt

# 4. Critical Libraries ko bina dependency check kiye install karo
# Taaki wo ladai na karein
RUN pip install av==10.0.0
RUN pip install --no-deps pytgcalls==3.0.0.dev18

# 5. Bot Start
CMD ["python", "main.py"]

