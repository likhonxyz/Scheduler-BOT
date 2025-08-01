from telethon import TelegramClient, events
import asyncio
import os

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION = os.getenv("SESSION")
client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)

scheduled_messages = []
message_delay = 10
active = True

@client.on(events.NewMessage(chats="YourControllerBotUsername"))
async def handler(event):
    global scheduled_messages, message_delay, active
    cmd = event.raw_text
    if cmd.startswith("/schedule "):
        parts = cmd.split(" ", 2)
        if len(parts) == 3:
            group, message = parts[1], parts[2]
            scheduled_messages.append((group, message))
            await event.reply(f"✅ Scheduled for {group}")
    elif cmd.startswith("/delay "):
        _, sec = cmd.split(" ", 1)
        message_delay = int(sec)
        await event.reply("✅ Delay updated")
    elif cmd == "/stop":
        active = False
        await event.reply("✅ Stopped.")

async def send_loop():
    global active
    while True:
        if active and scheduled_messages:
            group, message = scheduled_messages.pop(0)
            await client.send_message(group, message)
            await asyncio.sleep(message_delay)
        else:
            await asyncio.sleep(5)

async def main():
    await client.start()
    await client.send_message("me", "✅ Userbot Started")
    await send_loop()

client.loop.run_until_complete(main())
