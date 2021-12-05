from django.db import models


class FitnessTestResult(models.Model):
    student = models.ForeignKey(
        "Student",
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

    exercise = models.ForeignKey(
        'FitnessTestExercise',
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )

    value = models.IntegerField(
        null=True,
        blank=True
    )
