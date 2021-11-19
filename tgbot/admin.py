from django.contrib import admin

from .models import StorageUser, Storage, StoredThing, Orders


class StorageUserAdmin(admin.ModelAdmin):
    list_display = [
        'telegram_id', 'username', 'first_name', 'last_name',
        'birth_date', 'DUL_series', 'DUL_number',
    ]


class StorageAdmin(admin.ModelAdmin):
    list_display = [
        'storage_name', 'storage_address',
    ]


class StoredThingAdmin(admin.ModelAdmin):
    list_display = [
        'thing_name', 'seasonal', 'tariff1', 'tariff2', 'from_month',
    ]


class OrdersAdmin(admin.ModelAdmin):
    list_display = [
        'order_num', 'order_date', 'storage', 'user', 'seasonal_store',
        'thing',
    ]
    fields = [
        'order_date', 'storage', 'user', 'seasonal_store', 'thing',
        'other_type_size', 'seasonal_things_count', 'store_duration',
        'summa'
    ]


admin.site.register(StorageUser, StorageUserAdmin)
admin.site.register(Storage, StorageAdmin)
admin.site.register(StoredThing, StoredThingAdmin)
admin.site.register(Orders, OrdersAdmin)
