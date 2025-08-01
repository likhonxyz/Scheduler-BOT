import os
import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession

api_id = int(os.environ.get("API_ID"))
api_hash = os.environ.get("API_HASH")
session_string = os.environ.get("SESSION_STRING")

client = TelegramClient(StringSession(session_string), api_id, api_hash)

async def main():
    await client.start()
    print("✅ Userbot running...")

    while True:
        if os.path.exists("commands.txt"):
            with open("commands.txt", "r") as f:
                lines = f.readlines()
            open("commands.txt", "w").close()  # clear after reading
            for line in lines:
                try:
                    target, msg = line.strip().split("|", 1)
                    await client.send_message(target, msg)
                except Exception as e:
                    print("❌ Error sending message:", e)
        await asyncio.sleep(3)

with client:
    client.loop.run_until_complete(main())