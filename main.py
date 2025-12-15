import os
import asyncio
import random
from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls.types import MediaStream
from yt_dlp import YoutubeDL

# --- CONFIG ---
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

app = Client("YTShortsBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
call = PyTgCalls(app)

# --- YOUTUBE DOWNLOADER LOGIC ---
def get_random_short(chat_id):
    """
    YouTube par search karke random Short nikalta hai.
    """
    query = random.choice(["trending shorts", "funny shorts", "viral shorts", "status shorts"])
    
    ydl_opts = {
        'format': 'best[ext=mp4]', # Best Quality MP4
        'noplaylist': True,
        'quiet': True,
        'default_search': 'ytsearch5', # Top 5 results layega
        'outtmpl': f'downloads/short_{chat_id}.%(ext)s',
        'geo_bypass': True,
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            print(f"🔍 Searching YouTube for: {query}...")
            info = ydl.extract_info(query, download=False)
            
            # Search results mein se random video pick karo
            if 'entries' in info:
                video_entry = random.choice(info['entries'])
            else:
                video_entry = info

            video_url = video_entry['webpage_url']
            title = video_entry.get('title', 'YouTube Short')
            
            print(f"⬇️ Downloading: {title}")
            # Ab Download karo
            ydl.download([video_url])
            
            filename = f"downloads/short_{chat_id}.mp4"
            return filename, title, video_entry.get('uploader', 'Unknown')
            
    except Exception as e:
        print(f"❌ YT-DLP Error: {e}")
        return None, None, None

@app.on_message(filters.command("play") & filters.group)
async def play_shorts(client, message):
    chat_id = message.chat.id
    msg = await message.reply_text("🔄 **YouTube se Shorts dhoond raha hoon...**")

    # Download in thread
    file_path, title, channel = await asyncio.to_thread(get_random_short, chat_id)

    if not file_path:
        await msg.edit_text("❌ Video nahi mili. Dobara try karo.")
        return

    await msg.edit_text(f"▶️ **Playing:** {title}\n📺 **Channel:** {channel}")

    try:
        await call.join_group_call(
            chat_id,
            MediaStream(video=file_path, audio=file_path)
        )
    except Exception as e:
        # Agar already chal raha hai, toh stream change karo
        try:
            await call.change_stream(
                chat_id,
                MediaStream(video=file_path, audio=file_path)
            )
        except:
            await msg.edit_text(f"❌ Streaming Error: {e}")

if __name__ == "__main__":
    if not os.path.exists("downloads"):
        os.makedirs("downloads")
    
    print("🚀 YouTube Shorts Bot Started!")
    app.start()
    call.start()
    asyncio.get_event_loop().run_forever()
    
