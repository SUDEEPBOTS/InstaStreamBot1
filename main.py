import os
import asyncio
from dotenv import load_dotenv

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from py_tgcalls import PyTgCalls
from py_tgcalls.types.input_stream import AudioVideoPiped

# ================== ENV ==================
load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
SESSION_STRING = os.getenv("SESSION_STRING")

INSTA_USER = os.getenv("INSTA_USER")
INSTA_PASS = os.getenv("INSTA_PASS")

# ================== IMPORT HELPERS ==================
# helpers.py me ye functions hone chahiye
from helpers import (
    login_instagram,
    get_suggested_reels,
    download_video,
)

# ================== CLIENTS ==================
bot = Client(
    "bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
)

user = Client(
    "user",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION_STRING,
)

pytgcalls = PyTgCalls(user)

# ================== STATE ==================
CHAT_DATA = {}

# ================== BUTTONS ==================
def control_buttons():
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("⏮ Prev", callback_data="prev"),
                InlineKeyboardButton("⏭ Next", callback_data="next"),
            ],
            [
                InlineKeyboardButton("⏹ Stop", callback_data="stop"),
            ],
        ]
    )

# ================== STREAM FUNCTION ==================
async def play_reel(chat_id, reel, msg):
    try:
        await msg.edit_text("⬇️ **Downloading reel…**")

        file_path = await asyncio.to_thread(
            download_video, reel.pk, chat_id
        )

        await pytgcalls.join_group_call(
            chat_id,
            AudioVideoPiped(file_path),
        )

        return True
    except Exception as e:
        await msg.edit_text(f"❌ **Streaming error:** `{e}`")
        return False

# ================== COMMANDS ==================
@bot.on_message(filters.command("play") & filters.group)
async def play_cmd(_, message):
    chat_id = message.chat.id
    msg = await message.reply_text("🔄 **Fetching Instagram reels…**")

    # Insta login check
    if not login_instagram(INSTA_USER, INSTA_PASS):
        await msg.edit_text("❌ Instagram login failed.")
        return

    reels = await asyncio.to_thread(get_suggested_reels)

    if not reels:
        await msg.edit_text("❌ No reels found.")
        return

    CHAT_DATA[chat_id] = {
        "reels": reels,
        "index": 0,
    }

    success = await play_reel(chat_id, reels[0], msg)
    if success:
        await msg.edit_text(
            f"🎬 **Playing Reel 1**\n👤 {reels[0].user.username}",
            reply_markup=control_buttons(),
        )

@bot.on_callback_query()
async def callbacks(_, cb):
    chat_id = cb.message.chat.id

    if chat_id not in CHAT_DATA:
        await cb.answer("Session expired. Use /play again.", show_alert=True)
        return

    data = cb.data
    reels = CHAT_DATA[chat_id]["reels"]
    index = CHAT_DATA[chat_id]["index"]

    if data == "stop":
        await pytgcalls.leave_group_call(chat_id)
        CHAT_DATA.pop(chat_id, None)
        await cb.message.delete()
        return

    if data == "next":
        index += 1
        if index >= len(reels):
            more = await asyncio.to_thread(get_suggested_reels)
            if more:
                reels.extend(more)
            else:
                await cb.answer("No more reels.", show_alert=True)
                return

    if data == "prev":
        if index == 0:
            await cb.answer("This is first reel.", show_alert=True)
            return
        index -= 1

    CHAT_DATA[chat_id]["index"] = index
    reel = reels[index]

    await cb.answer("Loading…")
    await cb.message.edit_text("⬇️ **Downloading next reel…**")

    await play_reel(chat_id, reel, cb.message)

    await cb.message.edit_text(
        f"🎬 **Playing Reel {index + 1}**\n👤 {reel.user.username}",
        reply_markup=control_buttons(),
    )

@bot.on_message(filters.command("off") & filters.group)
async def stop_cmd(_, message):
    chat_id = message.chat.id
    try:
        await pytgcalls.leave_group_call(chat_id)
        CHAT_DATA.pop(chat_id, None)
        await message.reply_text("✅ VC stopped.")
    except Exception as e:
        await message.reply_text(f"❌ Error: `{e}`")

# ================== START ==================
async def main():
    print("🚀 Starting bot…")
    await user.start()
    await pytgcalls.start()
    await bot.start()
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
