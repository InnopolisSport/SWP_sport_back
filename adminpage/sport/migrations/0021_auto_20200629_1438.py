# Generated by Django 3.0.7 on 2020-06-29 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sport', '0020_add_medical_group'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='group',
            index=models.Index(fields=['name'], name='group_name_9aba6c_idx'),
        ),
        migrations.AddIndex(
            model_name='semester',
            index=models.Index(fields=['start'], name='semester_start_8aa8e0_idx'),
        ),
        migrations.AddIndex(
            model_name='sport',
            index=models.Index(fields=['name'], name='sport_name_ea8557_idx'),
        ),
        migrations.AddIndex(
            model_name='training',
            index=models.Index(fields=['group', 'start'], name='training_group_i_439792_idx'),
        ),
    ]
