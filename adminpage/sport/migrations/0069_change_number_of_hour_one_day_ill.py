# Generated by Django 3.1.8 on 2021-08-06 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sport', '0068_auto_20210802_1649'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='semester',
            name='number_hours_one_day_ill',
        ),
        migrations.AddField(
            model_name='semester',
            name='number_hours_one_week_ill',
            field=models.IntegerField(default=2),
        ),
    ]
