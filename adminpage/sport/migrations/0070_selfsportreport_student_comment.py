# Generated by Django 3.1.8 on 2021-08-07 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sport', '0069_change_number_of_hour_one_day_ill'),
    ]

    operations = [
        migrations.AddField(
            model_name='selfsportreport',
            name='student_comment',
            field=models.TextField(blank=True, max_length=1024, null=True),
        ),
    ]
