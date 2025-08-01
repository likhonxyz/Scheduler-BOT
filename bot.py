import os
from telegram import Update, InputMediaPhoto
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
import json
import asyncio

COMMAND_FILE = 'commands.json'
DELAY_FILE = 'delay.txt'

# Load or initialize delay
def get_delay():
    try:
        with open(DELAY_FILE, 'r') as f:
            return int(f.read())
    except:
        return 10

def save_command(command):
    try:
        with open(COMMAND_FILE, 'w') as f:
            json.dump(command, f)
    except Exception as e:
        print("Error saving command:", e)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Scheduler Bot is running!")

async def schedule(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        target = context.args[0]
        text = " ".join(context.args[1:])
        command = {"type": "text", "target": target, "text": text}
        save_command(command)
        await update.message.reply_text(f"✅ Scheduled message to {target}.")
    except:
        await update.message.reply_text("❌ Usage: /schedule <group_id_or_link> <message>")

async def schedulemedia(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if not update.message.reply_to_message or not update.message.reply_to_message.photo:
            await update.message.reply_text("❌ Please reply to an image with caption and use /schedulemedia <group_id_or_link>")
            return
        photo = update.message.reply_to_message.photo[-1]
        caption = update.message.caption or update.message.reply_to_message.caption or " "
        target = context.args[0]
        photo_file = await photo.get_file()
        file_path = f"media/{photo.file_unique_id}.jpg"
        os.makedirs("media", exist_ok=True)
        await photo_file.download_to_drive(file_path)
        command = {"type": "media", "target": target, "caption": caption, "file": file_path}
        save_command(command)
        await update.message.reply_text(f"✅ Scheduled media to {target}.")
    except Exception as e:
        await update.message.reply_text("❌ Usage: Reply to a photo and use /schedulemedia <group_id_or_link>")

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    save_command({"type": "stop"})
    await update.message.reply_text("🛑 Stopped all scheduled messages.")

async def delay(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        d = int(context.args[0])
        with open(DELAY_FILE, 'w') as f:
            f.write(str(d))
        await update.message.reply_text(f"⏱️ Delay set to {d} seconds.")
    except:
        await update.message.reply_text("❌ Usage: /delay <seconds>")

app = ApplicationBuilder().token(os.environ['BOT_TOKEN']).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("schedule", schedule))
app.add_handler(CommandHandler("schedulemedia", schedulemedia))
app.add_handler(CommandHandler("stop", stop))
app.add_handler(CommandHandler("delay", delay))
app.run_polling()