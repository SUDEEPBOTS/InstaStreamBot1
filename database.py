import os
import pymongo
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")

try:
    client = pymongo.MongoClient(MONGO_URL)
    db = client["InstaVCBot"]
    session_col = db["insta_session"]
    print("✅ MongoDB Connected Successfully")
except Exception as e:
    print(f"❌ MongoDB Error: {e}")

def save_insta_session(settings):
    # Purana session hata ke naya save karega
    session_col.delete_many({"type": "login"})
    session_col.insert_one({"type": "login", "settings": settings})

def load_insta_session():
    data = session_col.find_one({"type": "login"})
    if data:
        return data["settings"]
    return None
