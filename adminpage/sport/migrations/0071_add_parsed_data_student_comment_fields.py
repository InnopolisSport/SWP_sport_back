# Generated by Django 3.1.8 on 2021-08-07 22:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sport', '0070_selfsportreport_student_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='selfsportreport',
            name='parsed_data',
            field=models.JSONField(blank=True, null=True, verbose_name='Data from link'),
        ),
        migrations.AlterField(
            model_name='selfsportreport',
            name='student_comment',
            field=models.TextField(blank=True, max_length=1024, null=True, verbose_name="Student's comment"),
        ),
    ]
