# Generated by Django 3.1.8 on 2021-08-13 08:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sport', '0077_add_increase_course'),
    ]

    operations = [
        migrations.CreateModel(
            name='Debt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('debt', models.IntegerField(default=0)),
                ('semester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sport.semester')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sport.student')),
            ],
            options={
                'verbose_name_plural': 'debts',
                'db_table': 'debt',
            },
        ),
    ]