import os
import asyncio
from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls.types import MediaStream

# Tumhara helper file import kiya
from helper import login_instagram, get_suggested_reels, download_video

# Config
API_ID = int(os.getenv("API_ID", "12345"))
API_HASH = os.getenv("API_HASH", "your_hash")
BOT_TOKEN = os.getenv("BOT_TOKEN", "your_token")
USERNAME = os.getenv("INSTA_USER")
PASSWORD = os.getenv("INSTA_PASS")

app = Client("InstaStreamBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
call = PyTgCalls(app)

# Bot Start hote hi Instagram Login karega
async def start_bot():
    print("🤖 Bot Starting...")
    login_instagram(USERNAME, PASSWORD)
    await app.start()
    await call.start()
    print("✅ Bot Started & Instagram Logged In!")
    # Bot ko rok ke rakhne ke liye
    await asyncio.Event().wait()

@app.on_message(filters.command("play") & filters.group)
async def play_insta_stream(client, message):
    chat_id = message.chat.id
    status_msg = await message.reply_text("🔄 Getting Instagram Reels...")

    # 1. Reels Fetch karo
    reels = get_suggested_reels()
    if not reels:
        await status_msg.edit_text("❌ Koi Reel nahi mili.")
        return

    # Pehli reel uthao
    reel = reels[0] 
    
    try:
        # 2. Download karo (Tumhare helper function se)
        file_path = download_video(reel.pk, chat_id)
        
        await status_msg.edit_text("▶️ Streaming starting...")

        # 3. Voice Chat mein Stream karo
        await call.join_group_call(
            chat_id,
            MediaStream(
                file_path,
            )
        )
    except Exception as e:
        await status_msg.edit_text(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(start_bot())
    
