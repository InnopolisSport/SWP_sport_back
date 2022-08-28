from django.db import models
from .enums import ExerciseTypeChoices


class PowerZone(models.Model):
    number = models.IntegerField(null=False, primary_key=True)
    description = models.TextField(null=True, blank=True)  # tinymce
    pulse = models.IntegerField(null=False, help_text="per 10 sec")
    ratio = models.FloatField(null=False)

    def __str__(self):
        return f"Z{self.number}"


class ExerciseParams(models.Model):
    exercise = models.ForeignKey('Exercise', on_delete=models.CASCADE, null=False)
    type = models.CharField(max_length=5, choices=ExerciseTypeChoices.choices, null=False)
    sport = models.ForeignKey('SportType', on_delete=models.CASCADE, null=False)
    power_zone = models.ForeignKey('PowerZone', on_delete=models.CASCADE, null=False)
    repeat = models.IntegerField(null=False)
    set = models.IntegerField(null=False, default=1)
    rest_interval = models.DurationField(null=False, help_text="in sec")

    def working_time(self):
        return self.repeat * self.set * self.exercise.avg_time

    def working_load(self):
        return self.working_time().total_seconds() * self.power_zone.pulse * self.power_zone.ratio * self.exercise.ratio


class Exercise(models.Model):
    name = models.CharField(max_length=50, null=False)  # same as style
    ratio = models.FloatField(null=False)
    avg_time = models.DurationField(null=False, help_text="per 10 sec")

    def __str__(self):
        return self.name


class SportType(models.Model):
    name = models.CharField(max_length=50, null=False)
    description = models.TextField(null=True, blank=True)  # tinymce

    def __str__(self):
        return self.name


class Training(models.Model):
    pass


class TrainingExercise(models.Model):
    training = models.ForeignKey('Training', on_delete=models.CASCADE, null=False)
    exercise = models.ForeignKey('ExerciseParams', on_delete=models.CASCADE, null=False)
    index = models.IntegerField(null=False, help_text="index of the exercise in the training")


class User(models.Model):
    name = models.CharField(max_length=50, null=False)
    student = models.OneToOneField('sport.Student', on_delete=models.SET_NULL, null=True,
                                   related_name="training_suggestor_user")
    time_ratio = models.FloatField(null=False, default=1)  # how it should work?
    working_load_ratio = models.FloatField(null=False, default=1)  # how it should work?
