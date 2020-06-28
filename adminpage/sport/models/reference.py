import uuid

from django.db import models

from sport.models import validate_hours


def get_reference_path(instance, filename):
    ext = filename.split('.')[-1]
    return f'medical_references/{instance.semester.name}/{instance.student.pk}/{uuid.uuid4()}.{ext}'


class Reference(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE, null=False)
    semester = models.ForeignKey('Semester', on_delete=models.CASCADE, null=False)
    image = models.ImageField(upload_to=get_reference_path)
    hours = models.DecimalField(max_digits=3, decimal_places=2, default=0, validators=[validate_hours])
    uploaded = models.DateTimeField(auto_now_add=True, null=False)

    class Meta:
        db_table = "reference"
        verbose_name_plural = "medical references"
        indexes = [
            models.Index(fields=("hours", "uploaded")),
        ]

    def __str__(self):
        return f"{self.student}{self.uploaded} for {self.semester}"
