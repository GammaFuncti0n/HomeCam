import yaml
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from telegram.request import HTTPXRequest

from src.utils import setup_loggers
from src.handlers import start, snapshot
import os

setup_loggers('log')
with open("auth.yaml", 'r') as f:
    allowed_users = yaml.safe_load(f)['allowed_users']

def main():
    app = ApplicationBuilder().token(os.getenv('TG_TOKEN')).request(HTTPXRequest()).build()

    app.bot_data["allowed_users"] = allowed_users

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("snapshot", snapshot))

    app.run_polling()

if __name__ == "__main__":
    main()