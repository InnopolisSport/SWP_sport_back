from django.db import models


class FitnessTestSession(models.Model):
    date = models.DateTimeField(null=False)
    teacher = models.ForeignKey('Trainer', on_delete=models.SET_NULL, null=True, blank=True)
    semester = models.ForeignKey('Semester', on_delete=models.CASCADE, null=False, blank=False)
