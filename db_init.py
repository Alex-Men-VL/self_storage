import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'self_storage.settings')
django.setup()

from tgbot.models import StoredThing, Storage, StorageUser
from db_constants import (
    storages,
    stored_things,
    admins_id,
)


def init():
    for city, address in storages.items():
        Storage.objects.get_or_create(
            storage_name=city,
            storage_address=address
        )

    for name, property in stored_things.items():
        StoredThing.objects.get_or_create(
            thing_name=name,
            seasonal=property['seasonal'],
            tariff1=property['tariff1'],
            tariff2=property['tariff2']
        )

    for admin_id in admins_id:
        try:
            admin = StorageUser.objects.get(telegram_id=admin_id)
            admin.is_admin = True
            admin.save()
        except StorageUser.DoesNotExist:
            pass


if __name__ == '__main__':
    init()
