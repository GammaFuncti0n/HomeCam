from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import subprocess
import time
import logging

user_logger = logging.getLogger("user_requests")

def get_photo():
    filename = f"/photo_{int(time.time())}.jpg"

    subprocess.run([
        "ffmpeg",
        "-y",
        "-f", "v4l2",
        "-i", "/dev/video0",
        "-frames:v", "1",
        filename
    ], check=True)

    return filename

async def photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    allowed_users = context.bot_data["allowed_users"]
    try:
        if str(user.id) in allowed_users:
            path = get_photo()
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
        await update.message.reply_text(f"Error: {e}")
        user_logger.info(
            'ERROR: Can not take photo', 
            extra={
                "user_id": user.id,
                "username": user.username
            })