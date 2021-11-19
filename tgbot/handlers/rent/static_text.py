# Message text common
choose_address = 'Выберите адрес склада'
choose_category = 'Что хотите хранить?'
order_confirmation = 'Чтобы подтвердить заказ, нажмите на кнопку Забронировать.'

requests_fio = 'Введите ваше ФИО'
requests_fio_again = 'Введите ваше ФИО через пробелы'
request_contact = '''Введите номер телефона в формате (8**********)
Или нажмите на кнопку в нижнем меню для автоматического определения номер.'''
requests_dul = 'Введите серию и номер паспорта'
requests_dirthdate = 'Введите дату рождения в формате день.месяц.год'

personal_data_from_bd = '''Ваши личные данные:
ФИО: {last_name} {first_name} {middle_name}
Номер телефона: {phone_number}
Серия и номер паспорта: {dul_s} {dul_n}
Дата рождения: {birthdate}

Чтобы подтвердить или изменить данные, нажмите на кнопку внизу экрана.'''

# Text for the 'Другое' category
choose_dimensions = 'Выберите габаритность ячейки.'
choose_period_months_12 = 'Выберите период хранения.'

# Text for the 'Сезонные вещи' category
choose_stuff_category = 'Выберите категорию вещей для хранения.'
choose_stuff_count = '''Укажите их количество в сообщении.
{price}'''
choose_more_or_less_month = '''Выберите период хранения.
До одного месяцы можно хранить только лыжи, сноуборд и велосипеды.'''
specify_period = 'Уточните период хранения.'

# Button text
addresses = [
    'Москва',
    'Санкт-Петербург',
    'Сочи',
    'Екатеринбург',
]

categories = [
    'Сезонные вещи',
    'Другое',
]

reserve = [
    'Забронировать'
]

request_contact_button = [
    'Определить автоматически'
]

skip_change_pd = [
    'Подтвердить',
    'Изменить'
]

# Button text for the 'Другое' category
dimensions_price = {str(dimensions): 599 + 150 * (dimensions - 1) for
                    dimensions in range(1, 11)}
dimensions = [f'{str(number)} кв.м. - {dimensions_price[str(number)]} руб'
              for number in range(1, 11)]
period_12_months = [
    '1 месяц',
    '2 месяца',
    '3 месяца',
    '4 месяца',
    '5 месяцев',
    '6 месяцев',
    '7 месяц',
    '8 месяца',
    '9 месяца',
    '10 месяца',
    '11 месяцев',
    '12 месяцев',
]


# Button text for the 'Сезонные вещи' category
stuff_categories = [
    'Лыжи',
    'Сноуборд',
    'Велосипед',
    'Колеса',
]

more_or_less_month = [
    'До одного месяца',
    'От одного месяца',
]

period_3_weeks = [
    '1 неделя',
    '2 недели',
    '3 недели',
]
period_6_months = [
    '1 месяц',
    '2 месяца',
    '3 месяца',
    '4 месяца',
    '5 месяцев',
    '6 месяцев',
]

# 'Сезонные вещи' price
price = {
    'Лыжи': '1 лыжи - 100 р/неделя или 300 р/мес',
    'Сноуборд': '1 сноуборд - 100 р/неделя или 300 р/мес',
    'Колеса': '4 колеса - 200 р/мес',
    'Велосипед': '1 велосипед - 150 р/ неделя или 400 р/мес',
}

