import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# IMPORTANT: 'py-tgcalls' use karo, 'pytgcalls' nahi
from py_tgcalls import PyTgCalls
from py_tgcalls.types import MediaStream

from dotenv import load_dotenv

# Import Helpers
from helpers import login_instagram, get_suggested_reels, download_video

load_dotenv()

# --- SETUP ---
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
SESSION_STRING = os.getenv("SESSION_STRING")
INSTA_USER = os.getenv("INSTA_USER")
INSTA_PASS = os.getenv("INSTA_PASS")

# Login Insta First
if not login_instagram(INSTA_USER, INSTA_PASS):
    print("❌ Insta Login Failed. Exiting...")
    exit()

bot = Client("bot_session", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
user = Client("user_session", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)
app = PyTgCalls(user)  # PyTgCalls 'py-tgcalls' se aayega

# Format: {chat_id: {'reels': [], 'index': 0, 'msg_id': 123}}
CHAT_DATA = {}

# --- CORE FUNCTIONS ---

async def play_specific_reel(chat_id, reel_obj):
    try:
        # 1. Download
        file_path = await asyncio.to_thread(download_video, reel_obj.pk, chat_id)
        
        # 2. Stream
        await app.play(
            chat_id,
            MediaStream(video=file_path, audio=file_path)  # MediaStream bhi 'py-tgcalls' se aayega
        )
        return True
    except Exception as e:
        print(f"Streaming Error: {e}")
        return False

def get_control_buttons():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⏮ Piche", callback_data="prev"), 
         InlineKeyboardButton("Aage (Next) ⏭", callback_data="next")],
        [InlineKeyboardButton("❌ Band Karo (Stop)", callback_data="stop")]
    ])

# --- COMMANDS ---

@bot.on_message(filters.command("play") & filters.group)
async def start_bot(client, message):
    chat_id = message.chat.id
    msg = await message.reply_text("🔄 **Instagram se Reels la raha hoon...**")
    
    # Fetch Initial Reels
    reels = await asyncio.to_thread(get_suggested_reels)
    
    if not reels:
        await msg.edit_text("❌ Reels nahi mili. Insta issue.")
        return

    # Data Setup
    CHAT_DATA[chat_id] = {
        'reels': reels,
        'index': 0,
        'msg': msg
    }
    
    await msg.edit_text(f"⬇️ **Downloading Reel 1...**")
    
    # Play First
    await play_specific_reel(chat_id, reels[0])
    
    await msg.edit_text(
        f"🎬 **Playing Reel 1**\n👤 User: {reels[0].user.username}",
        reply_markup=get_control_buttons()
    )

@bot.on_callback_query()
async def handle_buttons(client, cb):
    chat_id = cb.message.chat.id
    data = cb.data
    
    if chat_id not in CHAT_DATA:
        await cb.answer("Session expired. /play again", show_alert=True)
        return

    ctx = CHAT_DATA[chat_id]
    reels = ctx['reels']
    index = ctx['index']
    msg = ctx['msg']

    if data == "stop":
        await app.leave_call(chat_id)
        del CHAT_DATA[chat_id]
        await msg.delete()
        return

    new_index = index

    if data == "next":
        new_index += 1
        # --- INFINITE LOOP LOGIC ---
        # Agar list khatam hone wali hai, toh aur fetch karo
        if new_index >= len(reels):
            await cb.answer("🔄 Loading MORE Reels...", show_alert=True)
            new_reels = await asyncio.to_thread(get_suggested_reels)
            if new_reels:
                reels.extend(new_reels) # Purani list mein nayi reels jod do
                CHAT_DATA[chat_id]['reels'] = reels # Update global data
            else:
                await cb.answer("❌ Aur reels nahi mili.", show_alert=True)
                return
        else:
            await cb.answer("Playing Next...")

    elif data == "prev":
        if index > 0:
            new_index -= 1
            await cb.answer("Playing Previous...")
        else:
            await cb.answer("Ye pehli reel hai!", show_alert=True)
            return

    # Update Index and Play
    CHAT_DATA[chat_id]['index'] = new_index
    current_reel = CHAT_DATA[chat_id]['reels'][new_index]
    
    # UI Update
    try:
        await msg.edit_text(f"⬇️ **Downloading...**")
        await play_specific_reel(chat_id, current_reel)
        await msg.edit_text(
            f"🎬 **Playing Reel {new_index + 1}**\n👤 User: {current_reel.user.username}",
            reply_markup=get_control_buttons()
        )
    except Exception as e:
        print(e)

@bot.on_message(filters.command("off") & filters.group)
async def stop_cmd(client, message):
    try:
        await app.leave_call(message.chat.id)
        if message.chat.id in CHAT_DATA:
            del CHAT_DATA[message.chat.id]
        await message.reply_text("✅ Stopped.")
    except:
        pass

print("🚀 Bot Started with Infinite Scroll!")
app.start()
bot.run()
