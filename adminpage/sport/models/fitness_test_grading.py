from django.db import models


class FitnessTestGrading(models.Model):
    exercise = models.ForeignKey(
        'FitnessTestExercise',
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )
    semester = models.ForeignKey(
        'Semester',
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )

    score = models.IntegerField()

    start_range = models.IntegerField()
    end_range = models.IntegerField()
