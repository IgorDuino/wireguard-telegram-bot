import os
import django
from telegram import Bot
from telegram.ext import Updater

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dtb.settings')
django.setup()

from dtb.settings import TELEGRAM_TOKEN
from tgbot.dispatcher import setup_dispatcher

bot_info = None
bot_link = None


def run_polling(tg_token: str = TELEGRAM_TOKEN):
    updater = Updater(tg_token, use_context=True)

    dp = updater.dispatcher
    dp = setup_dispatcher(dp)

    global bot_info
    bot_info = Bot(tg_token).get_me()
    global bot_link
    bot_link = f"https://t.me/{bot_info['username']}"

    print(f"Polling of '{bot_link}' has started")

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    run_polling()
