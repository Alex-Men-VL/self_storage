from telegram import ParseMode, Update
from telegram.ext import ConversationHandler

from tgbot.models import StorageUser
from tgbot.handlers.rent_common import static_text
from .keyboard_utils import (
    make_keyboard_with_addresses,
    make_keyboard_with_category,
    make_keyboard_with_dimensions,
    make_keyboard_with_stuff_categories,
)


ADDRESS, CATEGORY, OTHER, SEASONAL = range(4)


def send_message_with_addresses(update: Update, rent_description):
    text = static_text.choose_address
    update.message.reply_text(
        text=text,
        reply_markup=make_keyboard_with_addresses(),
    )
    return ADDRESS


def get_store_address(update: Update, rent_description):
    address = update.message.text
    rent_description.bot_data['address'] = address

    text = static_text.choose_category
    update.message.reply_text(
        text,
        reply_markup=make_keyboard_with_category()
    )
    return CATEGORY


def get_category(update: Update, rent_description):
    category = update.message.text
    rent_description.bot_data['category'] = category
    if category == static_text.categories[1]:
        text = static_text.choose_dimensions
        update.message.reply_text(
            text,
            reply_markup=make_keyboard_with_dimensions()
        )
        return OTHER
    elif category == static_text.categories[0]:
        text = static_text.choose_stuff_category
        update.message.reply_text(
            text,
            reply_markup=make_keyboard_with_stuff_categories()
        )
        return SEASONAL


def done(update: Update, rent_description):
    text = f'Адрес: {rent_description.bot_data["address"]}\n' \
           f'Категория: {rent_description.bot_data["category"]}'
    update.message.reply_text(text)
    return ConversationHandler.END


