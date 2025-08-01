import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession
import os
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION = os.getenv("SESSION")

client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)
controller_channel = os.getenv("CONTROLLER_CHANNEL", "me")

scheduled_commands = []

@client.on(events.NewMessage(chats=controller_channel))
async def handler(event):
    if event.text:
        print("Received command:", event.text)

async def main():
    await client.start()
    print("Userbot is running...")
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())