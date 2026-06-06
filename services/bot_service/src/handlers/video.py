from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import requests
import logging

#user_logger = logging.getLogger("bot")
session = requests.Session()
session.trust_env = False

async def video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    allowed_users = context.bot_data["allowed_users"]
    try:
        if str(user.id) in allowed_users:
            resp = session.post("http://camera_service:8000/video?duration=5", timeout=10)
            path = resp.json()["file"]
            await update.message.reply_video(video=open(path, "rb"), supports_streaming=True)
            logging.info(f"{user.id} | {user.username} | {path}")
        else:
            logging.warning(f"{user.id} | {user.username} | WARNING: Unknown user")

    except Exception as e:
        await update.message.reply_text(f"ERROR: {e}")
        logging.error(f"{user.id} | {user.username} | ERROR: {e}")