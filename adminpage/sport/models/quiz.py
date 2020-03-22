from datetime import datetime

from django.db import models


class Quiz(models.Model):
    author_id = models.ForeignKey("User", on_delete=models.SET_NULL, null=True)
    created = models.DateTimeField(default=datetime.now)
    active = models.BooleanField(default=True)

    class Meta:
        db_table = "quiz"
        verbose_name_plural = "quizzes"

    def __str__(self):
        return f"{self.created}"
