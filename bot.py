import os
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import asyncio

commands = {}
delay = 10  # default delay in seconds
looping = False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Scheduler Bot Active!\nUse /help to see commands.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""
📘 Available Commands:
/schedule <group> <message> - Start looped message sending.
/schedulemedia - Not supported in this version.
/delay <seconds> - Set delay between messages.
/stop - Stop the message loop.
/help - Show this message.
    """)

async def delay_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global delay
    if context.args:
        try:
            delay = int(context.args[0])
            await update.message.reply_text(f"⏱ Delay set to {delay} seconds.")
        except:
            await update.message.reply_text("❌ Invalid delay value.")
    else:
        await update.message.reply_text("ℹ Usage: /delay 10")

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global looping
    looping = False
    await update.message.reply_text("🛑 Loop stopped.")

async def schedule(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global looping
    if len(context.args) < 2:
        await update.message.reply_text("❌ Usage: /schedule <group_id_or_link> <message>")
        return

    target = context.args[0]
    msg = " ".join(context.args[1:])
    looping = True
    await update.message.reply_text(f"📤 Sending to {target} every {delay}s. Use /stop to end.")

    while looping:
        with open("commands.txt", "a") as f:
            f.write(f"{target}|{msg}\n")
        await asyncio.sleep(delay)

if __name__ == "__main__":
    bot_token = os.environ.get("BOT_TOKEN")
    app = ApplicationBuilder().token(bot_token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("delay", delay_command))
    app.add_handler(CommandHandler("stop", stop))
    app.add_handler(CommandHandler("schedule", schedule))

    app.run_polling()