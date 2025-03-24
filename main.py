import asyncio
import os
import random
import requests
import openai
from gtts import gTTS
from telethon import TelegramClient, events, functions
from dotenv import load_dotenv  # Load env variables

# 🔹 Load environment variables from config.env
load_dotenv("config.env")

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# OpenAI API Setup
openai.api_key = OPENAI_API_KEY

# 📲 Telegram Client
bot = TelegramClient('chatbot_session', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# 🎭 Sticker Collection
STICKERS = [
    "CAACAgUAAxkBAAEJmYxlKYVKh_d_5TkArQtMkSPyUnT4QAACaAoAApO4aFUs5T8-yxtM8y8E",
    "CAACAgEAAxkBAAEJmY1lKYWKjDXNLOV33PK5ZLqlg8_l-wACwwMAAvAuSULz6wtnbpGcmS8E",
    "CAACAgEAAxkBAAEJmY9lKYXQfHn1Us3DsqidMo2bc6nH1QACYAoAAm7ISUc0CHtrbEvM2i8E",
    "CAACAgEAAxkBAAEJmZBlKYX7HpTuU1hohMafoyLV_M2hbgACdA8AAm_hSUE3ht-KqEU9ji8E"
]

# 🎭 Female-Style Response Function
async def get_female_response(user_message):
    prompt = f"""
    Tu ek masti bhari ladki hai jo Telegram pe groups me chat karti hai.
    Teri baatein engaging, thodi flirty aur natural honi chahiye.
    Message: "{user_message}"
    Reply kar ek ladki ki tarah:
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"]

# 🎤 Convert Text to Voice (Female AI Voice)
def text_to_voice(text, filename="voice_reply.mp3"):
    tts = gTTS(text, lang="hi")  # Hinglish AI female voice
    tts.save(filename)
    return filename

# 🔄 Auto-Reply System (Text + Voice + Stickers)
@bot.on(events.NewMessage(pattern=".*"))
async def chat_handler(event):
    if event.is_group:
        user_msg = event.message.text
        sender = await event.get_sender()
        if sender.bot:
            return

        try:
            typing = asyncio.create_task(event.reply("💬 Typing..."))
            await asyncio.sleep(random.randint(2, 5))
            reply = await get_female_response(user_msg)
            await typing.cancel()

            action = random.choice(["text", "voice", "sticker"])

            if action == "voice":
                voice_file = text_to_voice(reply)
                await event.reply(file=voice_file)
            elif action == "sticker":
                sticker_id = random.choice(STICKERS)
                await event.reply(file=sticker_id)
            else:
                await event.reply(reply)

        except Exception as e:
            print(f"Error: {e}")  # Debugging ke liye
            await event.reply("😔 Sorry, abhi busy hoon!")

# 🔄 Change Profile Picture (DP)
@bot.on(events.NewMessage(pattern="/changedp"))
async def change_dp(event):
    sender = await event.get_sender()

    # ✅ Ensure only bot admin can change DP
    if not sender or not sender.is_self:
        return await event.reply("❌ Sirf bot admin DP change kar sakta hai!")

    # ✅ Download new DP from user's message
    if event.photo:
        photo = await event.download_media()
        
        try:
            # ✅ Change profile photo
            await bot(functions.photos.UploadProfilePhotoRequest(
                file=await bot.upload_file(photo)
            ))
            await event.reply("✅ DP Successfully Changed! 🎉")
        except Exception as e:
            await event.reply(f"❌ Error: {e}")
    else:
        await event.reply("❌ Please reply to a **photo** to change DP!")

# 🚀 Bot Start
async def main():
    print("💖 Hinglish ChatBot Ready!")
    await bot.run_until_disconnected()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
