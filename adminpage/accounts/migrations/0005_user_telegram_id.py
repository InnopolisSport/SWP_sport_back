# Generated by Django 3.1.8 on 2022-08-07 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20210610_2308'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='telegram_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]