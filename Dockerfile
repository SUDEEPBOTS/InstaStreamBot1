FROM python:3.10-slim-buster

WORKDIR /app

# 1. System updates aur FFmpeg install
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y ffmpeg git && apt-get clean

# 2. Files copy
COPY . .

# 3. Pip update
RUN pip install --no-cache-dir --upgrade pip

# 4. Critical Dependencies Install (Ye error fix karega)
# av 12.0.0 pre-built wheels use karta hai, toh pkg-config error nahi aayega
RUN pip install av==12.0.0 py-tgcalls==3.0.0.dev24

# 5. Baaki requirements
RUN pip install -r requirements.txt

# 6. Bot start
CMD ["python3", "main.py"]

