# 1. Base Image: Bookworm (Latest & Stable)
FROM python:3.10-slim-bookworm

WORKDIR /app

# 2. System updates + Build Tools + RUST (Ye hai Magic Fix!)
# 'build-essential' C++ ke liye, 'cargo' aur 'rustc' Rust ke liye
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y ffmpeg git build-essential python3-dev cargo rustc && apt-get clean

# 3. Files copy
COPY . .

# 4. Pip update
RUN pip install --no-cache-dir --upgrade pip

# 5. Libraries Install
# Ab hum wapas LATEST code use kar sakte hain
# Kyunki ab hamare paas 'cargo' hai, toh wo 'ntgcalls' khud bana lega
RUN pip install av==12.0.0
RUN pip install git+https://github.com/pytgcalls/pytgcalls.git

# 6. Baaki requirements
RUN pip install -r requirements.txt

# 7. Bot start
CMD ["python3", "main.py"]

