# 1. Base Image
FROM python:3.10-slim-bookworm

WORKDIR /app

# 2. System updates + Build Tools
# 'cmake' add kiya hai (Ye MISSING tha, isliye error aa raha tha)
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y ffmpeg git build-essential python3-dev cargo rustc cmake && apt-get clean

# 3. Files copy
COPY . .

# 4. Pip update & Maturin
RUN pip install --no-cache-dir --upgrade pip
RUN pip install maturin

# 5. Dependency Installation
# Ab 'cmake' hai, toh ye bina roye install ho jayega
RUN pip install av==12.0.0
RUN pip install git+https://github.com/pytgcalls/ntgcalls.git
RUN pip install git+https://github.com/pytgcalls/pytgcalls.git

# 6. Baaki requirements
RUN pip install -r requirements.txt

# 7. Bot start
CMD ["python3", "main.py"]

