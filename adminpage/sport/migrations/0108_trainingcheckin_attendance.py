# Generated by Django 3.1.8 on 2022-05-22 10:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sport', '0107_trainingcheckin'),
    ]

    operations = [
        migrations.AddField(
            model_name='trainingcheckin',
            name='attendance',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='checkin', to='sport.attendance'),
        ),
    ]
