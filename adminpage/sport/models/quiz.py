from django.db import models
from datetime import datetime


class Quiz(models.Model):
    author_id = models.ForeignKey("User", on_delete=models.SET_NULL, null=False)
    created = models.DateTimeField(default=datetime.now)
    active = models.BooleanField(default=True)

    class Meta:
        db_table = "quiz"

    def __str__(self):
        return f"{self.created}"
