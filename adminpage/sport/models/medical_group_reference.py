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

    resolved = models.BooleanField(
        default=False,
    )

    semester = models.ForeignKey(
        "Semester",
        on_delete=models.CASCADE,
    )

    def save(self, *args, **kwargs, ) -> None:
        # fixme hardcoded bind to object
        self.resolved = self.student.medical_group_id != -2
        return super().save(*args, **kwargs)

    class Meta:
        db_table = "medical_group_reference"
