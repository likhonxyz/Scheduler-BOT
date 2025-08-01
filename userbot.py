from telethon import TelegramClient, events
import asyncio
import os

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION = os.getenv("SESSION")

client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)

message_loops = {}
DELAY = 10

@client.on(events.NewMessage(from_users=int(os.getenv("BOT_UID"))))
async def handler(event):
    global DELAY
    if event.message.message.startswith("/schedule "):
        parts = event.message.message.split(" ", 2)
        if len(parts) < 3:
            return await event.reply("Usage: /schedule <group> <delay> <message>")
        target, delay, msg = parts[1], int(parts[2].split(" ")[0]), " ".join(parts[2].split(" ")[1:])
        async def send_loop():
            while True:
                try:
                    await client.send_message(target, msg)
                    await asyncio.sleep(delay)
                except asyncio.CancelledError:
                    break
        if target in message_loops:
            message_loops[target].cancel()
        task = asyncio.create_task(send_loop())
        message_loops[target] = task
        await event.reply(f"Scheduled message every {delay}s to {target}")

    elif event.message.message.startswith("/stop "):
        target = event.message.message.split(" ", 1)[1]
        if target in message_loops:
            message_loops[target].cancel()
            del message_loops[target]
            await event.reply(f"Stopped sending messages to {target}")

    elif event.message.message.startswith("/delay "):
        DELAY = int(event.message.message.split(" ")[1])
        await event.reply(f"Global delay set to {DELAY}s")

with client:
    print("Userbot is running...")
    client.run_until_disconnected()