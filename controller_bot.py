import os
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(TOKEN)
application = Application.builder().token(TOKEN).build()
app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
async def webhook():
    if request.method == "POST":
        update = Update.de_json(request.get_json(force=True), bot)
        await application.process_update(update)
        return "ok"

scheduled_messages = []
message_delay = 10  # default delay

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
ℹ️ এই বটের ব্যবহারবিধি:

/schedule <group_id/group_link> <message>
  ➤ নির্দিষ্ট গ্রুপে মেসেজ পাঠানোর জন্য

/schedulemedia <group_id/group_link> <caption>
  ➤ মিডিয়া সহ মেসেজ পাঠাতে (মিডিয়া attach করে পাঠাও)

/delay <seconds>
  ➤ দুই মেসেজের মাঝে বিরতি নির্ধারণ করতে

/stop
  ➤ চলমান মেসেজ পাঠানো বন্ধ করতে
"""
    await update.message.reply_text(help_text)

application.add_handler(CommandHandler("help", help_command))

if __name__ == "__main__":
    application.run_webhook(
        listen="0.0.0.0",
        port=int(os.getenv("PORT", "8443")),
        webhook_url=os.getenv("WEBHOOK_URL") + "/webhook"
                      )
