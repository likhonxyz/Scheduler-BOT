import asyncio
import json
import os
import time
from telethon import TelegramClient
from telethon.sessions import StringSession

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
session = os.getenv("SESSION")

client = TelegramClient(StringSession(session), api_id, api_hash)

if not os.path.exists("commands.json"):
    with open("commands.json", "w") as f:
        json.dump([], f)
if not os.path.exists("delay.txt"):
    with open("delay.txt", "w") as f:
        f.write("10")

async def main_loop():
    await client.start()
    print("Userbot started...")
    while True:
        try:
            with open("commands.json", "r") as f:
                data = json.load(f)
            with open("delay.txt", "r") as f:
                delay = int(f.read().strip())
            for item in data:
                try:
                    await client.send_message(item["group"], item["msg"])
                    print(f"Sent to {item['group']}: {item['msg']}")
                except Exception as e:
                    print(f"Error sending to {item['group']}: {e}")
                time.sleep(delay)
        except Exception as e:
            print("Loop error:", e)
        await asyncio.sleep(5)

with client:
    client.loop.run_until_complete(main_loop())
