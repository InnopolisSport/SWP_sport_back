# Generated by Django 3.1.8 on 2022-08-27 00:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sport', '0111_auto_20220825_1430'),
    ]

    operations = [
        migrations.CreateModel(
            name='Exercise',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('ratio', models.FloatField()),
                ('avg_time', models.DurationField(help_text='per 10 sec')),
            ],
        ),
        migrations.CreateModel(
            name='ExerciseParams',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('WU', 'Warmup'), ('PS', 'Preset'), ('MS', 'Main set'), ('CD', 'Cooldown')], max_length=5)),
                ('repeat', models.IntegerField()),
                ('set', models.IntegerField(default=1)),
                ('rest_interval', models.DurationField(help_text='in sec')),
                ('exercise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='training_suggestor.exercise')),
            ],
        ),
        migrations.CreateModel(
            name='PowerZone',
            fields=[
                ('number', models.IntegerField(primary_key=True, serialize=False)),
                ('description', models.TextField(blank=True, null=True)),
                ('pulse', models.IntegerField(help_text='per 10 sec')),
                ('ratio', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='SportType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Training',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('time_ratio', models.FloatField(default=1)),
                ('working_load_ratio', models.FloatField(default=1)),
                ('student', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='training_suggestor_user', to='sport.student')),
            ],
        ),
        migrations.CreateModel(
            name='TrainingExercise',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.IntegerField(help_text='index of the exercise in the training')),
                ('exercise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='training_suggestor.exerciseparams')),
                ('training', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='training_suggestor.training')),
            ],
        ),
        migrations.AddField(
            model_name='exerciseparams',
            name='power_zone',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='training_suggestor.powerzone'),
        ),
        migrations.AddField(
            model_name='exerciseparams',
            name='sport',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='training_suggestor.sporttype'),
        ),
    ]