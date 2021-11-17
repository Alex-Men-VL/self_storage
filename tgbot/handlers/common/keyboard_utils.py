from telegram import ReplyKeyboardMarkup, KeyboardButton

from .static_text import addresses


def build_menu(buttons, n_cols,
               header_buttons=None,
               footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, [header_buttons])
    if footer_buttons:
        menu.append([footer_buttons])
    return menu


def make_keyboard_for_start_command() -> ReplyKeyboardMarkup:
    buttons = [KeyboardButton(address) for address in addresses]

    reply_markup = ReplyKeyboardMarkup(
        build_menu(buttons, n_cols=2),
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return reply_markup
