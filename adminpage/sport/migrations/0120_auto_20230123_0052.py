# Generated by Django 3.1.8 on 2023-01-22 21:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sport', '0119_group_accredited'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='accredited',
            field=models.BooleanField(default=True),
        ),
    ]