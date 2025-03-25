import os
import random
import asyncio
import time
from telethon import TelegramClient, events, functions
from openai import OpenAI
from gtts import gTTS
from dotenv import load_dotenv

load_dotenv()

# 🔥 API Keys
API_ID = 19485675
API_HASH = "14e59046dacdc958e5f1936019fb064b"
BOT_TOKEN = "8146390672:AAEnu0jemPtpWHVVIfVy68xj___NQu02imU"
OPENAI_API_KEY = "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"

# 🤖 Initialize Telegram Bot
client = TelegramClient("bot", API_ID, API_HASH).start(bot_token=BOT_TOKEN)
ai_client = OpenAI(api_key=OPENAI_API_KEY)

# 🎭 Custom Sticker Pack
stickers = [
    "CAACAgUAAxkBAAELe6VlX8CnQjCFbNq3J4bYcYGG-GYxXwACtwIAAnH9oFWI0Dvo-I_o_jAE",
    "CAACAgUAAxkBAAELe6hlX8Cp81oAF0Q0dfJKFbrgu0sxlAACpgIAAnH9oFVoPiT2PxuoHTAE"
]

# 📸 Auto DP Change Images
dp_images = ["dp1.jpg", "dp2.jpg", "dp3.jpg"]

# 🕐 Cooldown System
last_message_time = {}

# 🌟 Hinglish AI Chat Function
def get_ai_reply(user_message):
    prompt = f"Mix Hindi + English me ek smart aur funny reply de: {user_message}"
    response = ai_client.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=100
    )
    return response.choices[0].message.content.strip()

# 🔊 Generate Voice Reply
def generate_voice(text):
    tts = gTTS(text=text, lang="hi")
    voice_path = "voice_reply.mp3"
    tts.save(voice_path)
    return voice_path

# 🔄 Auto Profile Picture Change (Every Hour)
async def change_profile_pic():
    while True:
        image = random.choice(dp_images)
        try:
            await client(functions.photos.UploadProfilePhotoRequest(
                file=await client.upload_file(image)
            ))
            print(f"✅ Auto Profile Picture Updated: {image}")
        except Exception as e:
            print(f"⚠️ DP Change Error: {e}")
        await asyncio.sleep(3600)  # DP Change every 1 hour

# 📨 Handle Messages (Group & Private)
@client.on(events.NewMessage)
async def handle_message(event):
    global last_message_time
    user_id = event.sender_id
    current_time = time.time()

    # 🕐 Cooldown (5 sec per user)
    if user_id in last_message_time and (current_time - last_message_time[user_id]) < 5:
        return  

    last_message_time[user_id] = current_time  # Update last message time

    user_message = event.message.text.strip()
    if not user_message:
        return

    # 🤖 AI Reply
    ai_reply = get_ai_reply(user_message)

    # 📢 Group Message Log
    if event.is_group:
        print(f"📢 Group Message: {user_message}")
    else:
        print(f"👤 Private Message: {user_message}")

    # 📝 Send AI Reply
    await event.reply(ai_reply + " ❤️🥰")

    # 🎭 Send Random Sticker
    await asyncio.sleep(1)
    await client.send_file(event.chat_id, file=random.choice(stickers))

    # 🔊 Send Voice Message
    voice_file = generate_voice(ai_reply)
    await client.send_file(event.chat_id, voice_file, voice_note=True)

# 🔄 Manual DP Change Command
@client.on(events.NewMessage(pattern="/changedp"))
async def change_dp_command(event):
    chat_id = event.chat_id

    # 🔄 Random DP Select
    image = random.choice(dp_images)

    try:
        # 📸 DP Change Karna
        await client(functions.photos.UploadProfilePhotoRequest(
            file=await client.upload_file(image)
        ))
        print(f"✅ DP Changed: {image}")

        # 📤 Image Send Karna (Confirmation)
        await client.send_file(chat_id, image, caption="✨ DP Updated Successfully!")

    except Exception as e:
        print(f"⚠️ DP Change Error: {e}")
        await event.reply("❌ DP change failed, try again later!")

# 🚀 Start Bot
async def main():
    print("🤖 Bot is running in Groups & Private Chats...")
    asyncio.create_task(change_profile_pic())  # Auto DP Change Task
    await client.run_until_disconnected()

try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("❌ Bot Stopped")
except Exception as e:
    print(f"⚠️ Error: {e}")

load_dotenv()  # .env File Load Karna

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

print("🔍 API_ID:", API_ID)
print("🔍 API_HASH:", API_HASH)
print("🔍 BOT_TOKEN:", BOT_TOKEN[:10] + "******")  # Safe Print
print("🔍 OPENAI_API_KEY:", OPENAI_API_KEY[:10] + "******")  # Safe Print

if API_ID is None or API_HASH is None or BOT_TOKEN is None or OPENAI_API_KEY is None:
    raise ValueError("⚠️ ERROR: Environment variables missing! Check .env file or Railway settings.")

API_ID = int(API_ID)  # Convert API_ID to int
