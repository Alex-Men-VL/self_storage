from django.db import models
from django.utils import timezone


class StorageUser(models.Model):
    telegram_id = models.IntegerField(unique=True)
    username = models.CharField(
        max_length=64,
        null=True,
        blank=False,
        verbose_name='Имя пользователя'
    )
    first_name = models.CharField(
        max_length=256,
        null=True,
        blank=False,
        verbose_name='Имя'
    )
    middle_name = models.CharField(
        max_length=256,
        null=True,
        blank=True,
        verbose_name='Отчество'
    )
    last_name = models.CharField(
        max_length=256,
        null=True,
        blank=True,
        verbose_name='Фамилия'
    )
    birth_date = models.DateField(
        null=True,
        blank=True,
        verbose_name='Дата рождения'
    )
    phone_number = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        verbose_name='Телефон (+код xxx xxx-xx-xx)'
    )
    DUL_series = models.CharField(
        max_length=4,
        null=True,
        blank=True,
        verbose_name='Серия паспорта'
    )
    DUL_number = models.CharField(
        max_length=6,
        null=True,
        blank=True,
        verbose_name='Номер паспорта'
    )
    there_is_pd = models.BooleanField(
        null=False,
        default=False,
        verbose_name='Есть ли личные данные'
    )

    def __str__(self):
        if self.username:
            return f'@{self.username}'
        else:
            return f'{self.telegram_id}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Storage(models.Model):
    """
    Справочник складов с наименованием и адресом
    """
    storage_name = models.CharField(
        max_length=255,
        null=True,
        blank=False,
        unique=True,
        verbose_name='Наименование')
    storage_address = models.CharField(
        max_length=1024,
        null=True,
        blank=False,
        unique=True,
        verbose_name='Адрес')

    def __str__(self):
        if self.storage_name:
            return f'{self.storage_name}'
        else:
            return f'{self.id}'

    class Meta:
        verbose_name = 'Склад'
        verbose_name_plural = 'Склады'


class StoredThing(models.Model):
    """
    Справочник хранимых вещей
    """
    thing_name = models.CharField(
        max_length=255,
        null=True,
        blank=False,
        unique=True,
        verbose_name='Название вещи'
    )
    seasonal = models.BooleanField(
        null=False,
        default=False,
        verbose_name='Сезонная вещь'
    )
    tariff1 = models.IntegerField(
        null=False,
        default=0,
        verbose_name='Цена хранения за неделю/Первый кв. метр'
    )
    tariff2 = models.IntegerField(
        null=False,
        default=0,
        verbose_name='Цена хранения за месяц/Дельта за следующие кв. метры'
    )
    from_month = models.BooleanField(
        null=False,
        default=False,
        verbose_name='Можно хранить меньше месяца')

    def __str__(self):
        if self.thing_name:
            return f'{self.thing_name}'
        else:
            return f'{self.id}'

    def get_storage_tariff(self):
        cost = {}
        if self.tariff1 > 0:
            cost['tariff1'] = self.tariff1
        if self.tariff2 > 0:
            cost['tariff2'] = self.tariff2
        return cost

    def get_storage_cost(self, duration: int, is_month: bool, count: int):
        """
        Вычисление стоимости хранения.

        duration: int - длительность хранения, единиц
        is_month: bool - единица длительности хранения:
            True - месяц;
            False - неделя
        count: int - количество:
            if self.seasonal - штук сезонных вещей
            else - кв. метров
        """
        if self.seasonal:
            if is_month:
                return duration * self.tariff2 * count
            else:
                return duration * self.tariff1 * count
        else:
            if count > 1:
                return self.tariff1 * duration + \
                       self.tariff2 * (count - 1) * duration
            else:
                return self.tariff1 * duration

    class Meta:
        verbose_name = 'Хранимая вещь'
        verbose_name_plural = 'Хранимые вещи'


class Orders(models.Model):
    """
    Справочник заказов
    """
    order_num = models.CharField(
        max_length=10,
        unique=True,
        null=False,
        blank=False,
        default='1',
        verbose_name='Номер заказа')
    order_date = models.DateField(
        null=False,
        default=timezone.now,
        verbose_name='Дата заказа')
    storage = models.ForeignKey(
        Storage,
        on_delete=models.CASCADE,
        default=None,
        related_name='orders',
        verbose_name='Склад')
    user = models.ForeignKey(
        StorageUser,
        on_delete=models.CASCADE,
        related_name='users',
        verbose_name='Пользователь')
    seasonal_store = models.BooleanField(
        null=False,
        default=False,
        verbose_name='Сезонные вещи/другое')
    thing = models.ForeignKey(
        StoredThing,
        on_delete=models.CASCADE,
        related_name='things',
        verbose_name='Хранимая вещь')
    other_type_size = models.IntegerField(
        null=True,
        default=0,
        verbose_name='Габаритность ячейки')
    seasonal_things_count = models.IntegerField(
        null=True,
        verbose_name='Количество сезонных вещей')
    store_duration = models.IntegerField(
        null=True,
        verbose_name='Длительность хранения')
    summa = models.FloatField(
        null=False,
        default=0,
        verbose_name='Стоимость хранения')
    qr_code = models.BinaryField(
        max_length=8192,
        null=True,
        verbose_name='QR-код')

    def __str__(self):
        return f'{self.id}-' \
               f'{self.user}-' \
               f'{timezone.now().strftime("%Y-%m-%d")}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
