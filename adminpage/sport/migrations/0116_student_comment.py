# Generated by Django 3.1.8 on 2022-09-23 20:12

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('sport', '0115_fitnesstestsession_retake'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='comment',
            field=tinymce.models.HTMLField(blank=True, default='', null=True),
        ),
    ]
