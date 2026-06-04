from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import time
import requests
import logging

user_logger = logging.getLogger("user_requests")
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
            user_logger.info(
                path, 
                extra={
                    "user_id": user.id,
                    "username": user.username
                })
        else:
            user_logger.info(
                "WARNING: Unknown user", 
                extra={
                    "user_id": user.id,
                    "username": user.username
                })

    except Exception as e:
        await update.message.reply_text(f"ERROR: {e}")
        user_logger.info(
            'ERROR: Can not take photo', 
            extra={
                "user_id": user.id,
                "username": user.username
            })