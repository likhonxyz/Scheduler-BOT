import os
from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import json

COMMAND_FILE = "commands.json"

def load_commands():
    if os.path.exists(COMMAND_FILE):
        with open(COMMAND_FILE, "r") as f:
            return json.load(f)
    return {}

def save_commands(data):
    with open(COMMAND_FILE, "w") as f:
        json.dump(data, f)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to the Scheduler Bot!")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "/schedule <group_link_or_id> <delay_in_sec> <message> - Schedule a message\n"
        "/schedulemedia <group_link_or_id> <delay_in_sec> <caption> - Schedule media (attach file)\n"
        "/stop <group_link_or_id> - Stop messages to a group\n"
        "/delay <group_link_or_id> <new_delay> - Update delay for group\n"
    )
    await update.message.reply_text(help_text)

async def schedule(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 3:
        return await update.message.reply_text("Usage: /schedule <group> <delay> <message>")
    group, delay, *msg_parts = context.args
    message = " ".join(msg_parts)
    data = load_commands()
    data[group] = {"type": "text", "delay": int(delay), "message": message}
    save_commands(data)
    await update.message.reply_text(f"Scheduled message to {group} every {delay}s.")

async def schedulemedia(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 3 or not update.message.document and not update.message.photo:
        return await update.message.reply_text("Usage: /schedulemedia <group> <delay> <caption> with media attached.")
    group, delay, *caption_parts = context.args
    caption = " ".join(caption_parts)

    file_id = update.message.document.file_id if update.message.document else update.message.photo[-1].file_id

    data = load_commands()
    data[group] = {"type": "media", "delay": int(delay), "file_id": file_id, "caption": caption}
    save_commands(data)
    await update.message.reply_text(f"Scheduled media to {group} every {delay}s.")

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 1:
        return await update.message.reply_text("Usage: /stop <group>")
    group = context.args[0]
    data = load_commands()
    if group in data:
        del data[group]
        save_commands(data)
        await update.message.reply_text(f"Stopped messages to {group}.")
    else:
        await update.message.reply_text("No schedule found for this group.")

async def delay(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        return await update.message.reply_text("Usage: /delay <group> <new_delay>")
    group, new_delay = context.args
    data = load_commands()
    if group in data:
        data[group]["delay"] = int(new_delay)
        save_commands(data)
        await update.message.reply_text(f"Updated delay for {group} to {new_delay}s.")
    else:
        await update.message.reply_text("No schedule found for this group.")

app = ApplicationBuilder().token(os.getenv("BOT_TOKEN")).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("schedule", schedule))
app.add_handler(CommandHandler("schedulemedia", schedulemedia))
app.add_handler(CommandHandler("stop", stop))
app.add_handler(CommandHandler("delay", delay))

app.run_polling()
