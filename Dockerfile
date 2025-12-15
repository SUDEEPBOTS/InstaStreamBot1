FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

RUN pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt

# 尝试安装稳定版本，如果失败则安装开发版本
RUN pip install pytgcalls==2.1.0 || pip install pytgcalls==3.0.0.dev24

CMD ["python", "main.py"]
