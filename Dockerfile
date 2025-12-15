FROM python:3.10-slim-buster

WORKDIR /app

# 1. System updates aur FFmpeg install karna (Music/Video ke liye zaroori hai)
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y ffmpeg git && apt-get clean

# 2. Files copy karna
COPY . .

# 3. Pip update karna
RUN pip install --no-cache-dir --upgrade pip

# 4. MAIN FIX: Yahan wo versions hain jo error nahi denge
# av 12.0.0 pre-built hai (compile error nahi aayega)
# py-tgcalls dev24 stable hai
RUN pip install av==12.0.0 py-tgcalls==3.0.0.dev24

# 5. Baaki requirements install karna
RUN pip install -r requirements.txt

# 6. Bot start karna
CMD ["python3", "main.py"]

