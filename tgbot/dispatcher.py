import sys
import logging
from typing import Dict

from telegram import Bot, Update, BotCommand
from telegram.ext import (
    Updater, Dispatcher, Filters,
    CommandHandler, MessageHandler,
    CallbackQueryHandler,
)
import telegram.error

from self_storage.settings import TELEGRAM_TOKEN, DEBUG
from tgbot.handlers.common import handlers as common_handlers


def setup_dispatcher(dp):
    dp.add_handler(CommandHandler("start", common_handlers.command_start))
    return dp


def run_pooling():
    """ Run bot in pooling mode """
    updater = Updater(TELEGRAM_TOKEN, use_context=True)

    dp = updater.dispatcher
    dp = setup_dispatcher(dp)

    bot_info = Bot(TELEGRAM_TOKEN).get_me()
    bot_link = f'https://t.me/{bot_info["username"]}'

    print(f"Pooling of '{bot_link}' started")
    # it is really useful to send '👋' emoji to developer
    # when you run local test
    # bot.send_message(text='👋', chat_id=<YOUR TELEGRAM ID>)

    updater.start_polling()
    updater.idle()


bot = Bot(TELEGRAM_TOKEN)
try:
    TELEGRAM_BOT_USERNAME = bot.get_me()["username"]
except telegram.error.Unauthorized:
    logging.error(f"Invalid TELEGRAM_TOKEN.")
    sys.exit(1)


def set_up_commands(bot_instance: Bot) -> None:
    langs_with_commands: Dict[str, Dict[str, str]] = {
        'en': {
            'start': 'Start django bot 🚀',
        },
        'ru': {
            'start': 'Запустить django бота 🚀',
        }
    }

    bot_instance.delete_my_commands()
    for language_code in langs_with_commands:
        bot_instance.set_my_commands(
            language_code=language_code,
            commands=[
                BotCommand(command, description) for command, description in
                langs_with_commands[language_code].items()
            ]
        )


# WARNING: it's better to comment the line below in DEBUG mode.
# Likely, you'll get a flood limit control error, when restarting bot too often
set_up_commands(bot)

# n_workers = 0 if DEBUG else 4
# dispatcher = setup_dispatcher(Dispatcher(bot, update_queue=None, workers=n_workers, use_context=True))
