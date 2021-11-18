from telegram import ParseMode, Update
from telegram.ext import ConversationHandler

from tgbot.models import StorageUser
from tgbot.handlers.rent import static_text
from .keyboard_utils import (
    make_keyboard_with_addresses,
    make_keyboard_with_category,
    make_keyboard_with_dimensions,
    make_keyboard_with_stuff_categories,
    make_keyboard_with_confirmation,
    make_keyboard_with_period,
    make_keyboard_with_stuff_period_1,
    make_keyboard_with_stuff_period_2_weeks,
    make_keyboard_with_stuff_period_2_months,
    make_keyboard_with_skip_button,
)

(ADDRESS,
 CATEGORY,
 OTHER,
 SEASONAL,
 PERIOD,
 COUNT,
 PERIOD1,
 PERIOD2,
 FIO,
 PHONE,
 DUL,
 BIRTHDATE) = range(12)


def send_message_with_addresses(update: Update, _):
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


'''Ветка другое'''


def get_dimension(update: Update, rent_description):
    dimensions = update.message.text
    rent_description.bot_data['dimensions'] = dimensions.split(' - ')[0].split()

    text = static_text.choose_period_months_12
    update.message.reply_text(
        text,
        reply_markup=make_keyboard_with_period()
    )
    return PERIOD


def get_period(update: Update, rent_description):
    period = update.message.text
    rent_description.bot_data['period'] = period

    text = static_text.order_confirmation
    update.message.reply_text(
        text,
        reply_markup=make_keyboard_with_confirmation()
    )
    return FIO


'''Конец ветки другое'''

'''Ветка сезонные вещи'''


def get_stuff_category(update: Update, rent_description):
    stuff_category = update.message.text
    rent_description.bot_data['stuff_category'] = stuff_category

    text = static_text.choose_stuff_count.format(
        price=static_text.price[stuff_category]
    )
    update.message.reply_text(
        text
    )
    return COUNT


def get_stuff_count(update: Update, rent_description):
    stuff_count = update.message.text
    rent_description.bot_data['stuff_count'] = stuff_count

    text = static_text.choose_more_or_less_month
    update.message.reply_text(
        text,
        reply_markup=make_keyboard_with_stuff_period_1()
    )
    return PERIOD1


def get_period_name(update: Update, rent_description):
    period = update.message.text
    if period == static_text.more_or_less_month[0]:
        period_name = 'неделя'
        keyboard = make_keyboard_with_stuff_period_2_weeks()
    else:
        period_name = 'месяц'
        keyboard = make_keyboard_with_stuff_period_2_months()
    rent_description.bot_data['period_name'] = period_name

    text = static_text.specify_period
    update.message.reply_text(
        text,
        reply_markup=keyboard
    )
    return PERIOD2


def get_period_count(update: Update, rent_description):
    period_count = update.message.text
    rent_description.bot_data['period_count'] = period_count

    text = static_text.order_confirmation
    update.message.reply_text(
        text,
        reply_markup=make_keyboard_with_confirmation()
    )
    return FIO


'''Конец сезонные вещи другое'''

''' Начало сценария после нажатия кнопки Забронировать'''


'''Конец сценария'''


def done(update: Update, rent_description):
    print(rent_description.bot_data)
    return ConversationHandler.END
