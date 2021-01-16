import uuid

from django.db import models


def get_reference_path(instance, filename):
    ext = filename.split('.')[-1]
    return f'medical_references/{instance.semester.name}/{instance.student.pk}/{uuid.uuid4()}.{ext}'


class Reference(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE, null=False)
    semester = models.ForeignKey('Semester', on_delete=models.CASCADE, null=False)
    image = models.ImageField(upload_to=get_reference_path)
    hours = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    uploaded = models.DateTimeField(auto_now_add=True, null=False)
    approval = models.BooleanField(null=True)
    comment = models.TextField(max_length=1024, null=True, blank=True)

    class Meta:
        db_table = "reference"
        verbose_name_plural = "medical references"

    def save(self, *args, **kwargs):
        # update flag and approval only when object is created via API
        if not kwargs.get('force_insert', False):
            self.hours = max(self.hours, 0)
            self.approval = self.hours > 0
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student}{self.uploaded} for {self.semester}"
