# Generated by Django 3.1.8 on 2021-12-06 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sport', '0085_auto_20211206_1321'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='fitnesstestresult',
            constraint=models.UniqueConstraint(fields=('student', 'semester', 'exercise'), name='student_semester_exercise'),
        ),
    ]
