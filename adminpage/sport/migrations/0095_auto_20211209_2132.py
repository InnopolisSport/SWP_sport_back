# Generated by Django 3.1.8 on 2021-12-09 18:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sport', '0094_auto_20211209_2110'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student',
            old_name='is_ill',
            new_name='has_QR',
        ),
    ]
