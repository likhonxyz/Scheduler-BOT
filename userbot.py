import asyncio
import json
import os
from telethon import TelegramClient
from telethon.tl.functions.messages import ImportChatInviteRequest

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
SESSION = "user"

client = TelegramClient(SESSION, api_id, api_hash)

async def resolve_group(group):
    try:
        if group.startswith("https://t.me/+"):
            hash_part = group.split("+", 1)[1]
            return await client(ImportChatInviteRequest(hash_part))
        elif group.startswith("https://t.me/"):
            return await client.get_entity(group)
        elif group.isdigit() or group.startswith("-100"):
            return int(group)
        return group
    except Exception as e:
        print(f"Failed to resolve group {group}: {e}")
        return None

async def main():
    await client.start()
    print("Userbot started...")

    while True:
        try:
            with open("commands.json", "r") as f:
                commands = json.load(f)
        except:
            commands = {}

        for group, config in commands.items():
            entity = await resolve_group(group)
            if not entity:
                continue

            if config["type"] == "text":
                await client.send_message(entity, config["message"])
            elif config["type"] == "media":
                await client.send_file(entity, config["file_id"], caption=config["caption"])
            await asyncio.sleep(config["delay"])

        await asyncio.sleep(5)

with client:
    client.loop.run_until_complete(main())
