from django.contrib import admin

from .models import StorageUser, Storage, StoredThing, Orders


admin.site.register(StorageUser)
admin.site.register(Storage)
admin.site.register(StoredThing)
admin.site.register(Orders)
