# Generated by Django 3.1.8 on 2022-09-17 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sport', '0114_auto_20220825_2103'),
    ]

    operations = [
        migrations.AddField(
            model_name='fitnesstestsession',
            name='retake',
            field=models.BooleanField(default=False),
        ),
    ]
