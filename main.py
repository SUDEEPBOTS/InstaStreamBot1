import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pytgcalls import PyTgCalls
from pytgcalls.types import MediaStream
from dotenv import load_dotenv

# Helpers se functions import kar rahe hain
from helpers import login_instagram, get_suggested_reels, download_video

# .env load karna
load_dotenv()

# --- CONFIGURATION ---
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
SESSION_STRING = os.getenv("SESSION_STRING")
INSTA_USER = os.getenv("INSTA_USER", "user")
INSTA_PASS = os.getenv("INSTA_PASS", "pass")

# --- 1. INSTAGRAM LOGIN CHECK ---
# Bot start hone se pehle Insta login check karega
if not login_instagram(INSTA_USER, INSTA_PASS):
    print("❌ Critical Error: Instagram Login Failed.")
    # Hum exit nahi kar rahe taaki bot crash na ho, par warning de rahe hain
else:
    print("✅ Instagram Login Verified!")

# --- 2. TELEGRAM CLIENTS SETUP ---
bot = Client("bot_session", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# User Client (Fix: Session String Handling)
if SESSION_STRING:
    print("✅ Loading User Client...")
    user = Client(
        "user_client", 
        api_id=API_ID, 
        api_hash=API_HASH, 
        session_string=SESSION_STRING
    )
else:
    print("❌ Error: SESSION_STRING nahi mila! VC start nahi hoga.")
    exit()

# PyTgCalls Setup
app = PyTgCalls(user)

# --- 3. STATE MANAGEMENT ---
# Har chat ka data alag save hoga
CHAT_DATA = {}

# --- 4. STREAMING HELPER ---
async def play_reel(chat_id, reel_obj, message_to_edit):
    try:
        # Download (Async thread mein taaki bot na ruke)
        await message_to_edit.edit_text("⬇️ **Downloading Video...**")
        file_path = await asyncio.to_thread(download_video, reel_obj.pk, chat_id)
        
        # Stream
        await app.play(
            chat_id,
            MediaStream(
                video=file_path, 
                audio=file_path
            )
        )
        return True
    except Exception as e:
        print(f"Streaming Error: {e}")
        await message_to_edit.edit_text(f"❌ Error: {e}")
        return False

# --- 5. BUTTONS LAYOUT ---
def get_buttons():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⏮ Piche", callback_data="prev"), 
         InlineKeyboardButton("Aage (Next) ⏭", callback_data="next")],
        [InlineKeyboardButton("❌ Stop Streaming", callback_data="stop")]
    ])

# --- 6. COMMANDS ---

@bot.on_message(filters.command("play") & filters.group)
async def start_reels(client, message):
    chat_id = message.chat.id
    msg = await message.reply_text("🔄 **Fetching Reels from Instagram...**")
    
    # Get Reels
    reels = await asyncio.to_thread(get_suggested_reels)
    
    if not reels:
        await msg.edit_text("❌ Instagram se Reels fetch nahi ho payi. Session check karein.")
        return

    # Data Save
    CHAT_DATA[chat_id] = {
        'reels': reels,
        'index': 0,
        'msg_id': msg.id 
    }
    
    # Play First Reel
    reel = reels[0]
    success = await play_reel(chat_id, reel, msg)
    
    if success:
        await msg.edit_text(
            f"🎬 **Playing Reel 1**\n👤 By: {reel.user.username}",
            reply_markup=get_buttons()
        )

@bot.on_callback_query()
async def handle_callback(client, cb):
    chat_id = cb.message.chat.id
    data = cb.data
    
    if chat_id not in CHAT_DATA:
        await cb.answer("❌ Session expired. Type /play again.", show_alert=True)
        return

    # Data Retrieve
    reels = CHAT_DATA[chat_id]['reels']
    index = CHAT_DATA[chat_id]['index']
    
    # Handle Stop
    if data == "stop":
        await app.leave_call(chat_id)
        del CHAT_DATA[chat_id]
        await cb.message.delete()
        return

    new_index = index

    # Logic for Next/Prev
    if data == "next":
        new_index += 1
        # Infinite Scroll Logic: Agar list khatam hone wali hai, aur fetch karo
        if new_index >= len(reels):
            await cb.answer("🔄 Loading More Reels...", show_alert=False)
            more_reels = await asyncio.to_thread(get_suggested_reels)
            if more_reels:
                reels.extend(more_reels)
                CHAT_DATA[chat_id]['reels'] = reels # Update list
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

    # Agar index badla hai, toh play karo
    if new_index != index:
        CHAT_DATA[chat_id]['index'] = new_index
        next_reel = reels[new_index]
        
        try:
            # Message update
            await cb.message.edit_text(f"⬇️ **Downloading Reel {new_index + 1}...**")
            
            # Streaming Call
            await play_reel(chat_id, next_reel, cb.message)
            
            # Final UI Update
            await cb.message.edit_text(
                f"🎬 **Playing Reel {new_index + 1}**\n👤 By: {next_reel.user.username}",
                reply_markup=get_buttons()
            )
        except Exception as e:
            print(f"Callback Error: {e}")

@bot.on_message(filters.command("off") & filters.group)
async def stop_vc(client, message):
    try:
        await app.leave_call(message.chat.id)
        if message.chat.id in CHAT_DATA:
            del CHAT_DATA[message.chat.id]
        await message.reply_text("✅ VC Ended.")
    except Exception as e:
        await message.reply_text(f"Error: {e}")

# --- 7. START BOT ---
print("🚀 Bot Starting...")
app.start()
bot.run()

