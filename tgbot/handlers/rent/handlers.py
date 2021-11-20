from datetime import date

import phonenumbers
from telegram import ParseMode, ShippingOption, Update, ReplyKeyboardRemove, \
    LabeledPrice
from telegram.ext import CallbackContext, ConversationHandler

from self_storage.settings import PROVIDER_TOKEN
from tgbot.models import StorageUser, Orders
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
    make_keyboard_with_invoice,
)

from ..common.keyboard_utils import make_keyboard_for_start_command

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
 PAY) = range(15)


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
    rent_description.bot_data['user_telegram_id'] = update.message.from_user.id

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
    rent_description.bot_data['period_count'] = period.split(' ')[0]

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
    stuff_category = rent_description.bot_data['stuff_category']
    is_wheels = (stuff_category == 'Колеса')
    if is_wheels and int(stuff_count) % 4 != 0:
        text = static_text.choose_stuff_count_error_wheels
        update.message.reply_text(
            text
        )
        return COUNT

    if is_wheels:
        rent_description.bot_data['stuff_count'] = str(int(stuff_count) // 4)
    else:
        rent_description.bot_data['stuff_count'] = stuff_count

    text = static_text.choose_more_or_less_month
    update.message.reply_text(
        text,
        reply_markup=make_keyboard_with_stuff_period_1(is_wheels)
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

''' Начало сценария после нажатия кнопки Забронировать. Ввод личных данных'''


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
        text = 'Перейти к оплате'
        update.message.reply_text(text=text,
                                  reply_markup=make_keyboard_with_invoice())
        return PAY
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
    dul = update.message.text
    try:
        dul_series, dul_number = dul.split()
        if len(dul_series) != 4 or len(dul_number) != 6:
            raise ValueError
    except ValueError:
        text = static_text.requests_dul
        update.message.reply_text(
            text=text,
            reply_markup=ReplyKeyboardRemove()
        )
        return DUL

    user_pd.bot_data['dul_series'] = dul_series
    user_pd.bot_data['dul_number'] = dul_number

    text = static_text.requests_dirthdate
    update.message.reply_text(
        text=text
    )
    return BIRTHDATE


def get_birthdate(update: Update, user_pd):
    birth_date = update.message.text
    birth_date.replace(',', '.')
    try:
        day, month, year = birth_date.split('.')
        if len(day) > 2 or len(month) > 2 or len(year) != 4:
            raise ValueError
    except ValueError:
        text = static_text.requests_dirthdate
        update.message.reply_text(
            text=text
        )
        return BIRTHDATE
    user_pd.bot_data['birth_date_day'] = day
    user_pd.bot_data['birth_date_month'] = month
    user_pd.bot_data['birth_date_year'] = year
    user_pd.bot_data['telegram_id'] = update.message.from_user.id

    update_data_in_database(user_pd)

    text = 'Перейти к оплате'
    update.message.reply_text(text=text,
                              reply_markup=make_keyboard_with_invoice())

    return PAY


def update_data_in_database(user_pd):
    user = StorageUser.objects.get(telegram_id=user_pd.bot_data['telegram_id'])
    user.first_name = user_pd.bot_data['first_name']
    user.middle_name = user_pd.bot_data['middle_name']
    user.last_name = user_pd.bot_data['last_name']
    user.phone_number = user_pd.bot_data['phone_number']

    user.DUL_series = user_pd.bot_data['dul_series']
    user.DUL_number = user_pd.bot_data['dul_number']

    day, month, year = map(int, (
        user_pd.bot_data['birth_date_day'],
        user_pd.bot_data['birth_date_month'],
        user_pd.bot_data['birth_date_year']
    ))
    user.birth_date = date(year, month, day)

    user.there_is_pd = True

    user.save()


'''Конец сценария'''


'''Сценарий оплаты'''


def send_shipping_callback(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    title = static_text.pay_title

    period_count = context.bot_data['period_count']
    period_name = context.bot_data['period_name']
    correct_period = static_text.correct_names[f'{period_count} {period_name}']
    description = static_text.pay_description.format(
        correct_period=correct_period
    )
    # select a payload just for you to recognize its the donation from your bot
    payload = static_text.pay_payload
    # In order to get a provider_token see https://core.telegram.org/bots/payments#getting-a-token
    provider_token = PROVIDER_TOKEN
    currency = static_text.pay_currency

    price = 100  # TODO: поправить

    prices = [LabeledPrice("Цена", price * 100)]

    # optionally pass need_name=True, need_phone_number=True,
    # need_email=True, need_shipping_address=True, is_flexible=True
    context.bot.send_invoice(
        chat_id, title, description, payload, provider_token, currency, prices
    )


def shipping_callback(update: Update, context: CallbackContext) -> None:
    """Answers the ShippingQuery with ShippingOptions"""
    query = update.shipping_query
    # check the payload, is this from your bot?
    if query.invoice_payload != static_text.pay_payload:
        # answer False pre_checkout_query
        query.answer(ok=False, error_message=static_text.pay_error)
        return


# after (optional) shipping, it's the pre-checkout
def precheckout_callback(update: Update, context: CallbackContext) -> None:
    """Answers the PreQecheckoutQuery"""
    query = update.pre_checkout_query
    # check the payload, is this from your bot?
    if query.invoice_payload != static_text.pay_payload:
        # answer False pre_checkout_query
        query.answer(ok=False, error_message=static_text.pay_error)
    else:
        query.answer(ok=True)


# finally, after contacting the payment provider...
def successful_payment_callback(update: Update, rent_description: CallbackContext) -> None:
    """Confirms the successful payment."""
    # do something after successfully receiving payment?
    Orders.save_order(rent_description.bot_data)
    print(rent_description.bot_data)
    update.message.reply_text(static_text.pay_success,
                              reply_markup=make_keyboard_for_start_command())
    return ConversationHandler.END


'''Конец сценария оплаты'''


# def done(update: Update, rent_description):

