# Generated by Django 3.1.8 on 2021-08-12 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sport', '0075_replace_min_medical_to_m2m'),
    ]

    operations = [
        migrations.AddField(
            model_name='semester',
            name='nullify_groups',
            field=models.ManyToManyField(blank=True, to='sport.MedicalGroup'),
        ),
    ]
