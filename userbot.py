import asyncio
import os
from telethon import TelegramClient, events
from telethon.sessions import StringSession

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
session_str = os.getenv("SESSION_STRING")
client = TelegramClient(StringSession(session_str), api_id, api_hash)

scheduled = False
delay = 10

@client.on(events.NewMessage(pattern=r'^/schedule (.+?) (.+)', incoming=True))
async def schedule_handler(event):
    global scheduled
    target, msg = event.pattern_match.group(1), event.pattern_match.group(2)
    await event.reply(f"✅ Scheduled message to {target}")
    scheduled = True
    while scheduled:
        try:
            await client.send_message(target, msg)
            await asyncio.sleep(delay)
        except Exception as e:
            await event.reply(str(e))
            break

@client.on(events.NewMessage(pattern=r'^/schedulemedia (.+)', incoming=True))
async def schedule_media_handler(event):
    global scheduled
    if event.media:
        target = event.pattern_match.group(1)
        await event.reply(f"✅ Scheduled media to {target}")
        scheduled = True
        while scheduled:
            try:
                await client.send_file(target, event.media, caption=event.text)
                await asyncio.sleep(delay)
            except Exception as e:
                await event.reply(str(e))
                break
    else:
        await event.reply("❌ মিডিয়া attach করো।")

@client.on(events.NewMessage(pattern=r'^/stop', incoming=True))
async def stop_handler(event):
    global scheduled
    scheduled = False
    await event.reply("🛑 বন্ধ করা হয়েছে।")

@client.on(events.NewMessage(pattern=r'^/delay (\d+)', incoming=True))
async def delay_handler(event):
    global delay
    delay = int(event.pattern_match.group(1))
    await event.reply(f"⏱️ Delay set to {delay} seconds.")

client.start()
print("Userbot is running...")
client.run_until_disconnected()
