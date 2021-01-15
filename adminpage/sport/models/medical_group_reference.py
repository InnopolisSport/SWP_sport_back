import uuid

from django.db import models


def get_reference_path(instance, filename):
    ext = filename.split('.')[-1]
    return f'medical_group_references/{instance.student.pk}/{uuid.uuid4()}.{ext}'


class MedicalGroupReference(models.Model):
    student = models.ForeignKey(
        "Student",
        on_delete=models.CASCADE,
    )

    image = models.ImageField(
        upload_to=get_reference_path,
    )

    resolved = models.BooleanField(null=True)

    semester = models.ForeignKey(
        "Semester",
        on_delete=models.CASCADE,
    )

    comment = models.TextField(max_length=1024, null=True, blank=True)

    def __str__(self):
        return f'{self.student} - {self.semester}'

    class Meta:
        db_table = "medical_group_reference"
