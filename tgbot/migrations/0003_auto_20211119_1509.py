# Generated by Django 3.2 on 2021-11-19 15:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tgbot', '0002_storageuser_there_is_pd'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orders',
            name='qr_code',
        ),
        migrations.AddField(
            model_name='orders',
            name='store_duration_type',
            field=models.CharField(choices=[('0', 'неделя'), ('1', 'месяц')], default='0', max_length=1, verbose_name='Единица длительности хранения'),
        ),
        migrations.AlterField(
            model_name='orders',
            name='thing',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='tgbot.storedthing', verbose_name='Хранимая вещь'),
        ),
        migrations.AlterField(
            model_name='orders',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='tgbot.storageuser', verbose_name='Пользователь'),
        ),
    ]
