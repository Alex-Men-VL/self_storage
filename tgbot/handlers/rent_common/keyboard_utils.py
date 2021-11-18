from telegram import ReplyKeyboardMarkup, KeyboardButton

from .static_text import (
    addresses,
    categories,
    dimensions,
    stuff_categories,
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


# Branch 'Другое'
def make_keyboard_with_dimensions() -> ReplyKeyboardMarkup:
    buttons = [KeyboardButton(dimension) for dimension in dimensions]

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
