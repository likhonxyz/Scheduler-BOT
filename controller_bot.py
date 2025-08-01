import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

TOKEN = os.getenv("BOT_TOKEN")
application = Application.builder().token(TOKEN).build()

scheduled_messages = []
message_delay = 10
active = True

async def schedule(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global scheduled_messages
    if len(context.args) < 2:
        await update.message.reply_text("Usage: /schedule <group_id> <message>")
        return
    group_id = context.args[0]
    message_text = " ".join(context.args[1:])
    scheduled_messages.append((group_id, message_text))
    await update.message.reply_text(f"✅ Scheduled message to {group_id}.")

async def delay(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global message_delay
    if len(context.args) != 1 or not context.args[0].isdigit():
        await update.message.reply_text("Usage: /delay <seconds>")
        return
    message_delay = int(context.args[0])
    await update.message.reply_text(f"✅ Delay set to {message_delay} seconds.")

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global active
    active = False
    await update.message.reply_text("✅ Message sending stopped.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ℹ️ Commands:
/schedule <group_id> <msg>
/delay <sec>
/stop")

application.add_handler(CommandHandler("schedule", schedule))
application.add_handler(CommandHandler("delay", delay))
application.add_handler(CommandHandler("stop", stop))
application.add_handler(CommandHandler("help", help_command))

application.run_polling()
