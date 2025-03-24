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
    You are a friendly, fun-loving female Telegram user chatting in a group. 
    Your responses should be engaging, slightly flirty, and natural.
    Message: "{user_message}"
    Reply like a girl: 
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"]

# 🎤 Convert Text to Voice (Female AI Voice)
def text_to_voice(text, filename="voice_reply.mp3"):
    tts = gTTS(text, lang="en")  # English AI female voice
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
            typing = asyncio.create_task(event.respond("💬 Typing..."))
            await asyncio.sleep(random.randint(2, 5))
            reply = await get_female_response(user_msg)
            await typing.cancel()

            action = random.choice(["text", "voice", "sticker"])

            if action == "voice":
                voice_file = text_to_voice(reply)
                await event.respond(file=voice_file)
            elif action == "sticker":
                sticker_id = random.choice(STICKERS)
                await event.respond(file=sticker_id)
            else:
                await event.respond(reply)

        except Exception as e:
            await event.respond("😔 Sorry, I'm busy right now!")

# 🚀 Bot Start
async def main():
    print("💖 Female ChatBot with Stickers & AI Running...")
    await bot.run_until_disconnected()

asyncio.run(main())
