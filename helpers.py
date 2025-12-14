import os
from instagrapi import Client
from database import save_insta_session, load_insta_session

cl = Client()

def login_instagram(username, password):
    print("🔄 Connecting to Instagram...")

    # --- PLAN A: Browser Cookie (Sabse Fast & Safe) ---
    session_id = os.getenv("INSTA_SESSIONID")
    
    if session_id:
        print("🍪 Found Browser Cookie! Logging in via Session ID...")
        try:
            # Direct Login via Cookie
            cl.login_by_sessionid(session_id)
            
            print("✅ Login Successful via Cookie!")
            
            # Future ke liye isko Database mein save kar lete hain
            try:
                save_insta_session(cl.dump_settings())
            except:
                pass
            return True
        except Exception as e:
            print(f"❌ Cookie Login Failed: {e}")

    # --- PLAN B: Database Check ---
    try:
        settings = load_insta_session()
        if settings:
            print("📥 Session found in DB! Loading...")
            cl.load_settings(settings)
            cl.login(username, password)
            return True
    except:
        pass

    # --- PLAN C: Username/Password (Jo fail ho raha tha) ---
    print("⚠️ Trying Username/Password Login...")
    try:
        cl.login(username, password)
        save_insta_session(cl.dump_settings())
        print("✅ New Login Successful")
        return True
    except Exception as e:
        print(f"❌ Login Failed: {e}")
        return False

def get_suggested_reels():
    try:
        return cl.clips_suggested(amount=5)
    except Exception as e:
        print(f"Error fetching reels: {e}")
        return []

def download_video(pk, chat_id):
    file_name = f"downloads/reel_{chat_id}.mp4"
    if os.path.exists(file_name):
        os.remove(file_name)
    
    if not os.path.exists("downloads"):
        os.makedirs("downloads")
        
    print(f"⬇️ Downloading Reel PK: {pk}")
    path = cl.video_download(pk, folder="downloads")
    os.rename(path, file_name)
    return file_name
    
