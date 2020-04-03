from django.db import models


class Admin(models.Model):
    first_name = models.CharField(max_length=50, null=False)
    last_name = models.CharField(max_length=50, null=False)
    email = models.CharField(max_length=50, null=False, unique=True)

    class Meta:
        db_table = "admin"
        verbose_name_plural = "admins"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
