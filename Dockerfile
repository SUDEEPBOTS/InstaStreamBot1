# 1. Base Image
FROM python:3.10-slim-bookworm

WORKDIR /app

# 2. System updates + Build Tools (Ye hai asli fix!)
# 'build-essential' aur 'python3-dev' zaroori hain jab koi library direct install na ho rahi ho
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y ffmpeg git build-essential python3-dev && apt-get clean

# 3. Files copy
COPY . .

# 4. Pip update
RUN pip install --no-cache-dir --upgrade pip

# 5. Libraries Install
# av 12.0.0 (Pre-built)
# git+... (Latest PyTgCalls code, ab ye build ho jayega)
RUN pip install av==12.0.0
RUN pip install git+https://github.com/pytgcalls/pytgcalls.git

# 6. Baaki requirements
RUN pip install -r requirements.txt

# 7. Bot start
CMD ["python3", "main.py"]

