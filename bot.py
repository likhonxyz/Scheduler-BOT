import os
import json
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

if not os.path.exists("commands.json"):
    with open("commands.json", "w") as f:
        json.dump([], f)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Scheduler Bot is Online!\nUse /schedule, /stop, /delay commands.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""
🛠 Command Guide:

/schedule <group_id/link> <message>
Example: /schedule -1001234567890 Hello World!

/schedule https://t.me/+abcDEFghiJKLmnop Hello!

/schedulemedia <group_id/link> <delay> <caption> (attach media)
Example: /schedulemedia -1001234567890 30s This is an image.

/stop <group_id/link>

/delay <seconds>
Example: /delay 20

🧠 Group ID or invite link supported.
📤 Media + caption supported.
    """)

async def delay_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        delay = int(context.args[0])
        with open("delay.txt", "w") as f:
            f.write(str(delay))
        await update.message.reply_text(f"✅ Delay set to {delay} seconds.")
    except:
        await update.message.reply_text("❌ Use: /delay <seconds>")

async def stop_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        group = context.args[0]
        with open("commands.json", "r") as f:
            data = json.load(f)
        data = [cmd for cmd in data if cmd["group"] != group]
        with open("commands.json", "w") as f:
            json.dump(data, f)
        await update.message.reply_text(f"🛑 Stopped messages to {group}.")
    except:
        await update.message.reply_text("❌ Use: /stop <group_id/link>")

async def schedule(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        group = context.args[0]
        msg = " ".join(context.args[1:])
        with open("commands.json", "r") as f:
            data = json.load(f)
        data.append({"group": group, "msg": msg})
        with open("commands.json", "w") as f:
            json.dump(data, f)
        await update.message.reply_text(f"✅ Scheduled message to {group}.")
    except:
        await update.message.reply_text("❌ Use: /schedule <group_id/link> <message>")

app = ApplicationBuilder().token(os.getenv("BOT_TOKEN")).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("schedule", schedule))
app.add_handler(CommandHandler("stop", stop_command))
app.add_handler(CommandHandler("delay", delay_command))
app.run_polling()
