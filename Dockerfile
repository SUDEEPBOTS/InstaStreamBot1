# 1. Base Image Change: Buster (purana) hata ke Bookworm (naya) lagaya hai
FROM python:3.10-slim-bookworm

WORKDIR /app

# 2. System updates (Ab ye 404 error nahi dega)
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y ffmpeg git && apt-get clean

# 3. Files copy
COPY . .

# 4. Pip update
RUN pip install --no-cache-dir --upgrade pip

# 5. Dependencies Fix:
# av==12.0.0 (ye binary hai, pkg-config error nahi dega)
# py-tgcalls==3.0.0.dev24 (stable version)
RUN pip install av==12.0.0 py-tgcalls==3.0.0.dev24

# 6. Baaki requirements
RUN pip install -r requirements.txt

# 7. Bot start
CMD ["python3", "main.py"]

