# Generated by Django 3.2.9 on 2021-11-21 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tgbot', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='storageuser',
            name='is_admin',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='Администратор'),
        ),
    ]
