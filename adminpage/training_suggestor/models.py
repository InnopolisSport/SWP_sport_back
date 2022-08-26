from django.db import models


class PowerZone(models.Model):
    number = models.IntegerField(null=False, unique=True)


class Exercise(models.Model):
    name = models.CharField(max_length=50, null=False)
    power_zone = models.ForeignKey(PowerZone, on_delete=models.CASCADE, null=False)


class ExerciseType(models.Model):
    type = models.CharField(max_length=50, null=False)
    description = models.TextField(null=True, blank=True)
    exercises = models.ManyToManyField(Exercise, blank=True)
