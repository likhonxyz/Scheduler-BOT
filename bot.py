from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os

# Global configs
DELAY = 10  # default delay in seconds

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Scheduler Bot is running.
Use /help to see available commands.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "🛠 *Scheduler Bot Commands*

"
        "/schedule <group_id_or_link> <delay> <message> - Schedule a message
"
        "/schedulemedia <group_id_or_link> <delay> <caption> (send media file with this command)
"
        "/stop <group_id_or_link> - Stop message loop
"
        "/delay <seconds> - Set global delay
"
    )
    await update.message.reply_text(help_text, parse_mode="Markdown")

if __name__ == '__main__':
    app = ApplicationBuilder().token(os.getenv("BOT_TOKEN")).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    print("Controller bot running...")
    app.run_polling()