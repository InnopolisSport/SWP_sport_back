# Generated by Django 3.1.8 on 2021-12-09 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sport', '0093_fitnesstestgrading_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='gender',
            field=models.IntegerField(choices=[(-1, 'unknown'), (0, 'male'), (1, 'female')], default=-1),
        ),
    ]
