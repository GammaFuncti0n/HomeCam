from telegram import Update
from telegram.ext import ContextTypes
import logging

user_logger = logging.getLogger("user_requests")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''
    Welcome message
    '''
    user = update.message.from_user
    allowed_users = context.bot_data["allowed_users"]
    if str(user.id) in allowed_users:
        text = (
            "Привет! Я бот, который делает снимок квартиры\n" \
            "для информации отправь `/start`\n"
            "для снимка отправь `/snapshot`\n"
        )
        await update.message.reply_text(text)
        user_logger.info(
            text, 
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