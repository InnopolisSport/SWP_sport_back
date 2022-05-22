from django.db import models


class TrainingCheckIn(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    student = models.ForeignKey("Student", on_delete=models.CASCADE, related_name='checkins')
    training = models.ForeignKey("Training", on_delete=models.CASCADE, related_name='checkins')
