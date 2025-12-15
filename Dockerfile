FROM python:3.10-slim

# System deps
RUN apt-get update && apt-get install -y ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

RUN pip install --upgrade pip setuptools wheel

# 🔥 INSTALL INSTAGRAPI WITHOUT DEPS (THIS KILLS av)
RUN pip install instagrapi==2.0.0 --no-deps

# बाकी सब normal
RUN pip install -r requirements.txt

CMD ["python", "main.py"]
