# > python manage.py shell
# from dbinit import init
# init()

from tgbot.models import StoredThing, Storage, Orders, StorageUser


def init():
    print('Инициализация данных...')

    print(' Очистка объектов:')
    print('  Склады...', end='')
    Storage.objects.all().delete()
    print(': Ок')
    print('  Хранимые вещи...', end='')
    StoredThing.objects.all().delete()
    print(': Ок')

    print(' Создание объектов:')
    print('  Склады...', end='')
    Storage(storage_name='Москва', storage_address='ул. Верхний тупик, д.13/7').save()
    Storage(storage_name='Санкт-Петербург', storage_address='Большой проспект Петроградской стороны, 37').save()
    Storage(storage_name='Сочи', storage_address='ул. Нижняя аллея, 18').save()
    Storage(storage_name='Екатеринбург', storage_address='ул. Героев Панфиловцев, 3').save()
    print(f': {Storage.objects.count()}')

    print('  Список хранимых вещей...', end='')
    StoredThing(thing_name='Другое', seasonal=False, tariff1=599, tariff2=150).save()
    StoredThing(thing_name='Лыжи', seasonal=True, tariff1=100, tariff2=300).save()
    StoredThing(thing_name='Сноуборд', seasonal=True, tariff1=100, tariff2=300).save()
    StoredThing(thing_name='Велосипед', seasonal=True, tariff1=150, tariff2=400).save()
    StoredThing(thing_name='Колёса (4 шт.)', seasonal=True, tariff1=0, tariff2=200).save()
    print(f': {StoredThing.objects.count()}')
    print('Инициализация завершена')

    print('Примеры использования')
    print('Тарифы на хранение:')
    thing = 'Лыжи'
    print(f'{thing}: {StoredThing.objects.get(thing_name=thing).get_storage_tariff()}')
    thing = 'Колёса (4 шт.)'
    print(f'{thing}: {StoredThing.objects.get(thing_name=thing).get_storage_tariff()}')
    thing = 'Другое'
    print(f'{thing}: {StoredThing.objects.get(thing_name=thing).get_storage_tariff()}')

    print('Стоимость хранения:')
    thing = 'Лыжи'
    print(f'{thing}: {StoredThing.objects.get(thing_name=thing).get_storage_cost(2, False, 1)}')
    print(f'{thing}: {StoredThing.objects.get(thing_name=thing).get_storage_cost(1, False, 2)}')
    print(f'{thing}: {StoredThing.objects.get(thing_name=thing).get_storage_cost(2, True, 1)}')
    print(f'{thing}: {StoredThing.objects.get(thing_name=thing).get_storage_cost(1, True, 2)}')
    thing = 'Колёса (4 шт.)'
    print(f'{thing}: {StoredThing.objects.get(thing_name=thing).get_storage_cost(3, True, 1)}')
    thing = 'Другое'
    print(f'{thing}: {StoredThing.objects.get(thing_name=thing).get_storage_cost(3, True, 2)}')
