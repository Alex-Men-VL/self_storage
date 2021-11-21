import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'self_storage.settings')
django.setup()


from tgbot.models import StoredThing, Storage, StorageUser


def init():
    Storage.objects.all().delete()
    StoredThing.objects.all().delete()

    Storage(storage_name='Москва',
            storage_address='ул. Верхний тупик, д.13/7').save()
    Storage(storage_name='Санкт-Петербург',
            storage_address='Большой проспект Петроградской стороны, 37').save()
    Storage(storage_name='Сочи',
            storage_address='ул. Нижняя аллея, 18').save()
    Storage(storage_name='Екатеринбург',
            storage_address='ул. Героев Панфиловцев, 3').save()

    StoredThing(thing_name='Другое', seasonal=False, tariff1=599,
                tariff2=150).save()
    StoredThing(thing_name='Лыжи', seasonal=True, tariff1=100,
                tariff2=300).save()
    StoredThing(thing_name='Сноуборд', seasonal=True, tariff1=100,
                tariff2=300).save()
    StoredThing(thing_name='Велосипед', seasonal=True, tariff1=150,
                tariff2=400).save()
    StoredThing(thing_name='Колеса', seasonal=True, tariff1=0,
                tariff2=200).save()

    admins_id = [154383987, 386453509, 901108747]
    for admin_id in admins_id:
        admin = StorageUser.objects.get(telegram_id=admin_id)
        admin.is_admin = True
        admin.save()


if __name__ == '__main__':
    init()
