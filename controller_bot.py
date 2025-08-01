import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

HELP_TEXT = """ℹ️ এই বটের ব্যবহারবিধি:

/schedule <group_id/group_link> <message>
  ➤ নির্দিষ্ট গ্রুপে মেসেজ পাঠানোর জন্য

/schedulemedia <group_id/group_link> <caption>
  ➤ মিডিয়া সহ মেসেজ পাঠাতে (মিডিয়া attach করে পাঠাও)

/delay <seconds>
  ➤ দুই মেসেজের মাঝে বিরতি নির্ধারণ করতে

/stop
  ➤ চলমান মেসেজ পাঠানো বন্ধ করতে
"""

scheduled_commands = []

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(HELP_TEXT)

async def schedule(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text
    if len(msg.split()) < 3:
        return await update.message.reply_text("❌ সঠিক ফরম্যাট: /schedule <group_id> <message>")
    group = msg.split()[1]
    text = " ".join(msg.split()[2:])
    scheduled_commands.append({"type": "text", "group": group, "text": text})
    await update.message.reply_text(f"✅ Scheduled message to {group}.")

async def schedule_media(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message or not update.message.reply_to_message.effective_attachment:
        return await update.message.reply_text("❌ মিডিয়া সহ বার্তা পাঠাতে একটি মিডিয়াতে রিপ্লাই দিন।")
    media = update.message.reply_to_message
    group = update.message.text.split()[1]
    caption = " ".join(update.message.text.split()[2:])
    scheduled_commands.append({"type": "media", "group": group, "media": media, "caption": caption})
    await update.message.reply_text(f"✅ Scheduled media message to {group}.")

async def delay(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text
    if len(msg.split()) != 2 or not msg.split()[1].isdigit():
        return await update.message.reply_text("❌ সঠিক ফরম্যাট: /delay <seconds>")
    scheduled_commands.append({"type": "delay", "seconds": int(msg.split()[1])})
    await update.message.reply_text(f"✅ Delay set to {msg.split()[1]} seconds.")

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    scheduled_commands.clear()
    await update.message.reply_text("🛑 All scheduled messages stopped.")

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("schedule", schedule))
app.add_handler(CommandHandler("schedulemedia", schedule_media))
app.add_handler(CommandHandler("delay", delay))
app.add_handler(CommandHandler("stop", stop))

app.run_webhook(
    listen="0.0.0.0",
    port=int(os.environ.get("PORT", 8000)),
    webhook_url=WEBHOOK_URL,
)