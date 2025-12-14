import os
from instagrapi import Client
from database import save_insta_session, load_insta_session

# Instagrapi Client
cl = Client()

def login_instagram(username, password):
    print("🔄 Logging into Instagram...")
    
    # 1. Try to load saved session from MongoDB
    try:
        settings = load_insta_session()
        if settings:
            cl.load_settings(settings)
            cl.login(username, password)
            print("✅ Logged in using Saved Session (MongoDB)")
            return True
    except Exception as e:
        print(f"⚠️ Session Load Failed: {e}")

    # 2. New Login if session failed or not found
    try:
        cl.login(username, password)
        print("✅ New Login Successful")
        # Save new session to MongoDB
        save_insta_session(cl.dump_settings())
        return True
    except Exception as e:
        print(f"❌ Login Failed: {e}")
        return False

def get_suggested_reels():
    # 5 Reels ek baar mein layega
    try:
        return cl.clips_suggested(amount=5)
    except Exception as e:
        print(f"Error fetching reels: {e}")
        return []

def download_video(pk, chat_id):
    # Purani file delete karo space bachane ke liye
    file_name = f"downloads/reel_{chat_id}.mp4"
    if os.path.exists(file_name):
        os.remove(file_name)
    
    # Folder ensure karo
    if not os.path.exists("downloads"):
        os.makedirs("downloads")
        
    print(f"⬇️ Downloading Reel PK: {pk}")
    path = cl.video_download(pk, folder="downloads")
    
    # Rename karke fix naam dena zaroori hai streaming ke liye
    os.rename(path, file_name)
    return file_name
