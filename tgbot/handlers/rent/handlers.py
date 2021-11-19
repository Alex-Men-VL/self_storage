from datetime import date

import phonenumbers
from telegram import ParseMode, Update, ReplyKeyboardRemove
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
    make_keyboard_with_skip_change_pd,
    make_keyboard_to_get_contact,
)

(ADDRESS,
 CATEGORY,
 OTHER,
 SEASONAL,
 PERIOD,
 COUNT,
 PERIOD1,
 PERIOD2,
 PD,
 SELECT_PD,
 FIO,
 PHONE,
 DUL,
 BIRTHDATE,
 FINISH) = range(15)


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
    rent_description.bot_data[
        'dimensions'
    ] = dimensions.split(' - ')[0].split()[0]

    text = static_text.choose_period_months_12
    update.message.reply_text(
        text,
        reply_markup=make_keyboard_with_period()
    )
    return PERIOD


def get_period(update: Update, rent_description):
    period = update.message.text
    rent_description.bot_data['period_name'] = 'месяц'
    rent_description.bot_data['period_count'] = period

    text = static_text.order_confirmation
    update.message.reply_text(
        text,
        reply_markup=make_keyboard_with_confirmation()
    )
    return PD


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
    rent_description.bot_data['period_count'] = period_count.split()[0]

    text = static_text.order_confirmation
    update.message.reply_text(
        text,
        reply_markup=make_keyboard_with_confirmation()
    )
    return PD


'''Конец ветки сезонные вещи'''

''' Начало сценария после нажатия кнопки Забронировать'''


def send_message_with_pd(update: Update, _):
    user = StorageUser.objects.get(telegram_id=update.message.from_user.id)
    if user.there_is_pd:
        text = static_text.personal_data_from_bd.format(
            last_name=user.last_name,
            first_name=user.first_name,
            middle_name=user.middle_name,
            phone_number=user.phone_number,
            dul_s=user.DUL_series,
            dul_n=user.DUL_number,
            birthdate=user.birth_date
        )
        update.message.reply_text(
            text=text,
            reply_markup=make_keyboard_with_skip_change_pd()
        )
        return SELECT_PD
    else:
        text = static_text.requests_fio
        update.message.reply_text(
            text=text
        )
        return FIO


def get_action_with_pd(update: Update, _):
    if update.message.text == static_text.skip_change_pd[0]:
        return FINISH
    else:
        text = static_text.requests_fio
        update.message.reply_text(
            text=text
        )
        return FIO


def get_fio(update: Update, user_pd):
    fio = update.message.text
    try:
        last_name, first_name, middle_name = map(
            lambda x: x.title(), fio.split()
        )
    except ValueError:
        text = static_text.requests_fio_again
        update.message.reply_text(
            text=text
        )
        return FIO
    user_pd.bot_data['first_name'] = first_name
    user_pd.bot_data['middle_name'] = middle_name
    user_pd.bot_data['last_name'] = last_name

    text = static_text.request_contact
    update.message.reply_text(
        text=text,
        reply_markup=make_keyboard_to_get_contact()
    )
    return PHONE


def get_contact(update: Update, user_pd):
    # TODO: Проверка на валидность
    try:
        phone_number = update.message.contact.phone_number
    except AttributeError:
        phone_number = update.message.text
    phonenumber = phone_number.replace('+', '').replace('-', '')
    if not phonenumber.isdigit() or len(phonenumber) < 11:
        text = static_text.request_contact
        update.message.reply_text(
            text=text,
            reply_markup=make_keyboard_to_get_contact()
        )
        return PHONE
    pure_phonenumber = phonenumbers.parse(phonenumber, 'RU')
    if phonenumbers.is_valid_number(pure_phonenumber):
        normalize_phonenumber = phonenumbers.format_number(
            pure_phonenumber,
            phonenumbers.PhoneNumberFormat.E164
        )
        user_pd.bot_data['phone_number'] = normalize_phonenumber
    else:
        text = static_text.request_contact
        update.message.reply_text(
            text=text,
            reply_markup=make_keyboard_to_get_contact()
        )
        return PHONE

    text = static_text.requests_dul
    update.message.reply_text(
        text=text,
        reply_markup=ReplyKeyboardRemove()
    )
    return DUL


def get_dul(update: Update, user_pd):
    # TODO: Проверка на валидность
    dul = update.message.text
    user_pd.bot_data['dul'] = dul

    text = static_text.requests_dirthdate
    update.message.reply_text(
        text=text
    )
    return BIRTHDATE


def get_birthdate(update: Update, user_pd):
    # TODO: Проверка на валидность
    birth_date = update.message.text
    user_pd.bot_data['birth_date'] = birth_date
    user_pd.bot_data['telegram_id'] = update.message.from_user.id

    update_data_in_database(user_pd)
    return FINISH


def update_data_in_database(user_pd):
    user = StorageUser.objects.get(telegram_id=user_pd.bot_data['telegram_id'])
    user.first_name = user_pd.bot_data['first_name']
    user.middle_name = user_pd.bot_data['middle_name']
    user.last_name = user_pd.bot_data['last_name']
    user.phone_number = user_pd.bot_data['phone_number']

    dul = user_pd.bot_data['dul'].split()
    user.DUL_series = dul[0]
    user.DUL_number = dul[1]

    day, month, year = map(int, user_pd.bot_data['birth_date'].split('.'))
    user.birth_date = date(year, month, day)

    user.there_is_pd = True

    user.save()


'''Конец сценария'''


def done(update: Update, rent_description):
    print(rent_description.bot_data)
    return ConversationHandler.END
