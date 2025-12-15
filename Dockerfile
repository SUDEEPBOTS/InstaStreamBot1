# 1. Base Image: Bookworm (Latest working Linux)
FROM python:3.10-slim-bookworm

WORKDIR /app

# 2. System updates aur Git install
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y ffmpeg git && apt-get clean

# 3. Files copy
COPY . .

# 4. Pip update
RUN pip install --no-cache-dir --upgrade pip

# 5. MAIN FIX HERE:
# Hum specific 'v3.0.0.dev21' tag install kar rahe hain.
# Ye version purane 'ntgcalls' (jo available hai) ke saath chalta hai.
RUN pip install av==12.0.0 git+https://github.com/pytgcalls/pytgcalls.git@v3.0.0.dev21

# 6. Baaki requirements
RUN pip install -r requirements.txt

# 7. Bot start
CMD ["python3", "main.py"]

