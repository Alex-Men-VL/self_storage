from telegram import ReplyKeyboardMarkup, KeyboardButton

from .static_text import (
    addresses,
    categories,
    dimensions,
    stuff_categories,
    period_12_months,
    reserve,
    more_or_less_month,
    period_3_weeks,
    period_6_months,
)


def build_menu(buttons, n_cols,
               header_buttons=None,
               footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, [header_buttons])
    if footer_buttons:
        menu.append([footer_buttons])
    return menu


def make_keyboard_with_addresses() -> ReplyKeyboardMarkup:
    buttons = [KeyboardButton(address) for address in addresses]

    reply_markup = ReplyKeyboardMarkup(
        build_menu(buttons, n_cols=2),
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return reply_markup


def make_keyboard_with_category() -> ReplyKeyboardMarkup:
    buttons = [KeyboardButton(category) for category in categories]

    reply_markup = ReplyKeyboardMarkup(
        build_menu(buttons, n_cols=2),
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return reply_markup


def make_keyboard_with_confirmation() -> ReplyKeyboardMarkup:
    buttons = [KeyboardButton(reser) for reser in reserve]

    reply_markup = ReplyKeyboardMarkup(
        build_menu(buttons, n_cols=2),
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return reply_markup


# Branch 'Другое'
def make_keyboard_with_dimensions() -> ReplyKeyboardMarkup:
    buttons = [KeyboardButton(dimension) for dimension in dimensions]

    reply_markup = ReplyKeyboardMarkup(
        build_menu(buttons, n_cols=2),
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return reply_markup


def make_keyboard_with_period() -> ReplyKeyboardMarkup:
    buttons = [KeyboardButton(address) for address in period_12_months]

    reply_markup = ReplyKeyboardMarkup(
        build_menu(buttons, n_cols=2),
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return reply_markup


# Branch 'Сезонные вещи'
def make_keyboard_with_stuff_categories() -> ReplyKeyboardMarkup:
    buttons = [KeyboardButton(category) for category in stuff_categories]

    reply_markup = ReplyKeyboardMarkup(
        build_menu(buttons, n_cols=2),
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return reply_markup


def make_keyboard_with_stuff_period_1() -> ReplyKeyboardMarkup:
    buttons = [KeyboardButton(choose) for choose in more_or_less_month]

    reply_markup = ReplyKeyboardMarkup(
        build_menu(buttons, n_cols=2),
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return reply_markup


def make_keyboard_with_stuff_period_2_weeks() -> ReplyKeyboardMarkup:
    buttons = [KeyboardButton(week) for week in period_3_weeks]

    reply_markup = ReplyKeyboardMarkup(
        build_menu(buttons, n_cols=1),
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return reply_markup


def make_keyboard_with_stuff_period_2_months() -> ReplyKeyboardMarkup:
    buttons = [KeyboardButton(month) for month in period_6_months]

    reply_markup = ReplyKeyboardMarkup(
        build_menu(buttons, n_cols=2),
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return reply_markup
