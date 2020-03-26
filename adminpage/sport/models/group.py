from django.db import models


class Group(models.Model):
    name = models.CharField(max_length=50, null=False)
    description = models.CharField(max_length=1000, null=True)
    sport = models.ForeignKey('Sport', on_delete=models.CASCADE, null=False)
    semester = models.ForeignKey('Semester', on_delete=models.CASCADE, null=False)
    trainer = models.ForeignKey('Trainer', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = "group"
        verbose_name_plural = "groups"

    def __str__(self):
        return f"{self.name}"
