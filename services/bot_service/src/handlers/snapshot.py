from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import time
import requests
import logging

#user_logger = logging.getLogger("bot")
session = requests.Session()
session.trust_env = False

async def snapshot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    allowed_users = context.bot_data["allowed_users"]
    try:
        if str(user.id) in allowed_users:
            resp = session.post("http://camera_service:8000/snapshot", timeout=5)
            path = resp.json()["file"]
            await update.message.reply_photo(photo=open(path, "rb"))
            logging.info(f"{user.id} | {user.username} | {path}")
        else:
            logging.warning(f"{user.id} | {user.username} | WARNING: Unknown user")

    except Exception as e:
        await update.message.reply_text(f"ERROR: {e}")
        logging.error(f"{user.id} | {user.username} | ERROR: {e}")