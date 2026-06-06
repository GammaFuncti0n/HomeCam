from telegram import Update
from telegram.ext import ContextTypes
import logging

#user_logger = logging.getLogger("bot")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''
    Welcome message
    '''
    user = update.message.from_user
    allowed_users = context.bot_data["allowed_users"]
    if str(user.id) in allowed_users:
        text = (
            "Привет! Я бот, который делает снимок квартиры\n" \
            "для информации отправь /start\n" \
            "для снимка отправь /snapshot\n" \
            "для 5 секундного видео отправь /video"
        )
        await update.message.reply_text(text)
        logging.info(f"{user.id} | {user.username} | {text}")
    else:
        logging.warning(f"{user.id} | {user.username} | WARNING: Unknown user")