from django.db import models


class User(models.Model):
    user_id = models.IntegerField(primary_key=True)  # telegram_id
    username = models.CharField(max_length=32, null=True, blank=True)
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256, null=True, blank=True)

    def __str__(self):
        if self.username:
            return f'@{self.username}'
        else:
            return f'{self.user_id}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
