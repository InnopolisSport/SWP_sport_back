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

    session = models.ForeignKey(
        'FitnessTestSession',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    value = models.IntegerField(
        null=True,
        blank=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['student', 'semester', 'exercise'], name='student_semester_exercise')
        ]
