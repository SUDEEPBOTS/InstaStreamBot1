# 1. Base Image
FROM python:3.10-slim-bookworm

WORKDIR /app

# 2. System updates (Sirf FFmpeg aur Git chahiye)
RUN apt-get update && apt-get install -y ffmpeg git && apt-get clean

# 3. Files copy
COPY . .

# 4. Pip update
RUN pip install --no-cache-dir --upgrade pip

# 5. Requirements install
RUN pip install -r requirements.txt

# 6. Bot start
CMD ["python3", "main.py"]

