# Generated by Django 3.1.8 on 2021-12-09 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sport', '0092_student_gender'),
    ]

    operations = [
        migrations.AddField(
            model_name='fitnesstestgrading',
            name='gender',
            field=models.IntegerField(choices=[(-1, 'both'), (0, 'male'), (1, 'female')], default=-1),
            preserve_default=False,
        ),
    ]
