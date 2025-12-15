# 1. Base Image: Bookworm (Latest working Linux)
FROM python:3.10-slim-bookworm

WORKDIR /app

# 2. System updates aur Git install karna (Git zaroori hai niche wale step ke liye)
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y ffmpeg git && apt-get clean

# 3. Files copy
COPY . .

# 4. Pip update
RUN pip install --no-cache-dir --upgrade pip

# 5. MAIN FIX HERE:
# Hum 'av' install kar rahe hain
# Aur 'py-tgcalls' seedha GitHub se utha rahe hain taaki version ka error na aaye
RUN pip install av==12.0.0 git+https://github.com/pytgcalls/pytgcalls.git

# 6. Baaki requirements
RUN pip install -r requirements.txt

# 7. Bot start
CMD ["python3", "main.py"]

