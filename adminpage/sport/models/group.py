from django.db import models


class Group(models.Model):
    name = models.CharField(max_length=50, null=False)
    description = models.CharField(max_length=1000, null=True, blank=True)
    capacity = models.PositiveIntegerField(default=50, null=False)
    is_club = models.BooleanField(default=False, null=False)
    sport = models.ForeignKey('Sport', on_delete=models.CASCADE, null=False)
    semester = models.ForeignKey('Semester', on_delete=models.CASCADE, null=False)
    trainer = models.ForeignKey('Trainer', on_delete=models.SET_NULL, null=True, blank=True)

    minimum_medical_group = models.ForeignKey('MedicalGroup', on_delete=models.DO_NOTHING, default=-2)

    class Meta:
        db_table = "group"
        verbose_name_plural = "groups"
        indexes = [
            models.Index(fields=("name",)),
        ]

    def __str__(self):
        return f"[{self.semester}] {self.name}"
