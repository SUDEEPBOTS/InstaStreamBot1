import os
import requests
from instagrapi import Client
from database import save_insta_session, load_insta_session

cl = Client()

def login_instagram(username, password):
    print("🔄 Connecting to Instagram...")

    session_id = os.getenv("INSTA_SESSIONID")

    # 1. Try Session ID (Cookie)
    if session_id:
        try:
            cl.login_by_sessionid(session_id)
            save_insta_session(cl.dump_settings())
            print("✅ Login via Cookie Successful")
            return True
        except Exception as e:
            print(f"Cookie login failed: {e}")

    # 2. Try Database Session
    try:
        settings = load_insta_session()
        if settings:
            cl.load_settings(settings)
            cl.login(username, password)
            print("✅ Login via DB session successful")
            return True
    except:
        pass

    # 3. Fresh Login (Username/Password)
    try:
        cl.login(username, password)
        save_insta_session(cl.dump_settings())
        print("✅ Fresh login successful")
        return True
    except Exception as e:
        print(f"❌ Login failed: {e}")
        return False


def get_suggested_reels():
    try:
        # 5 reels fetch karega
        return cl.clips_suggested(amount=5)
    except Exception as e:
        print(f"Error fetching reels: {e}")
        return []


def download_video(pk, chat_id):
    if not os.path.exists("downloads"):
        os.makedirs("downloads")

    file_path = f"downloads/reel_{chat_id}.mp4"
    
    # Purana file delete karo taaki overwrite ho sake
    if os.path.exists(file_path):
        os.remove(file_path)

    print(f"⬇️ Fetching Reel URL for PK: {pk}")

    # 🔥 SAFE: Fresh URL fetch kar rahe hain
    media = cl.media_info(pk)
    video_url = media.video_url

    if not video_url:
        raise Exception("No video URL found")

    # Download using requests (No FFmpeg/AV errors)
    r = requests.get(video_url, stream=True, timeout=30)
    with open(file_path, "wb") as f:
        for chunk in r.iter_content(chunk_size=1024 * 1024):
            if chunk:
                f.write(chunk)

    return file_path
    
