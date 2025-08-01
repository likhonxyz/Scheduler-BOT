import asyncio, os, json
from telethon import TelegramClient

api_id = int(os.environ['API_ID'])
api_hash = os.environ['API_HASH']
session_string = os.environ['SESSION_STRING']
client = TelegramClient(StringSession(session_string), api_id, api_hash)

COMMAND_FILE = 'commands.json'
DELAY_FILE = 'delay.txt'

def get_delay():
    try:
        with open(DELAY_FILE, 'r') as f:
            return int(f.read())
    except:
        return 10

async def main_loop():
    await client.start()
    print("✅ Userbot running...")
    while True:
        try:
            if not os.path.exists(COMMAND_FILE):
                await asyncio.sleep(5)
                continue
            with open(COMMAND_FILE, 'r') as f:
                cmd = json.load(f)
            if cmd.get("type") == "stop":
                await asyncio.sleep(5)
                continue
            elif cmd.get("type") == "text":
                target = cmd['target']
                while True:
                    await client.send_message(target, cmd['text'])
                    await asyncio.sleep(get_delay())
            elif cmd.get("type") == "media":
                while True:
                    await client.send_file(cmd['target'], cmd['file'], caption=cmd.get('caption'))
                    await asyncio.sleep(get_delay())
        except Exception as e:
            print("Loop error:", e)
            await asyncio.sleep(5)

with client:
    client.loop.run_until_complete(main_loop())