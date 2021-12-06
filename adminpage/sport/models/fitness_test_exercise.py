from django.db import models


class FitnessTestExercise(models.Model):
    exercise_name = models.CharField(
        max_length=50,
        null=False,
        blank=False
    )

    value_unit = models.CharField(
        max_length=1000,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.exercise_name
