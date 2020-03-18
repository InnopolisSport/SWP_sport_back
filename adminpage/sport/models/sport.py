from django.db import models


class Sport(models.Model):
    name = models.CharField(max_length=50, null=False)

    class Meta:
        db_table = "sport"

    def __str__(self):
        return f"{self.name}"
