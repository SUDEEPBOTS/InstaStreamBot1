# 1. Base Image: Bookworm (Latest & Stable)
FROM python:3.10-slim-bookworm

WORKDIR /app

# 2. System updates + Build Tools + RUST (Zaroori hai build karne ke liye)
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y ffmpeg git build-essential python3-dev cargo rustc && apt-get clean

# 3. Files copy
COPY . .

# 4. Pip update & Maturin (Build system for Rust)
RUN pip install --no-cache-dir --upgrade pip
RUN pip install maturin

# 5. THE FIX: Pehle dependency banao, fir main library install karo
# Pehle 'ntgcalls' install kar rahe hain source se (jo version 2.0.7+ dega)
RUN pip install git+https://github.com/pytgcalls/ntgcalls.git

# Ab 'pytgcalls' install karo (Ab ye khush rahega kyunki ntgcalls mil jayega)
RUN pip install av==12.0.0
RUN pip install git+https://github.com/pytgcalls/pytgcalls.git

# 6. Baaki requirements
RUN pip install -r requirements.txt

# 7. Bot start
CMD ["python3", "main.py"]

