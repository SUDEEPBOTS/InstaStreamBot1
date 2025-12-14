# Hum Bani-Banayi Image use kar rahe hain
# Isme Python + FFmpeg + PyTgCalls pehle se hai!
FROM pytgcalls/pytgcalls:latest

WORKDIR /app

# 1. Sirf Requirements install karo (cache clear karke RAM bachaane ke liye)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2. Code Copy karo
COPY . .

# 3. Start Command
CMD ["python", "main.py"]

