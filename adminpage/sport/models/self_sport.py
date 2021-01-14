import uuid

from django.db import models
from image_optimizer.fields import OptimizedImageField


def get_report_path(instance, filename):
    ext = filename.split('.')[-1]
    return f'self_sport_reports/{instance.semester.name}/' \
           f'{instance.student.pk}/{uuid.uuid4()}.{ext}'


class SelfSportReport(models.Model):
    student = models.ForeignKey(
        'Student',
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )
    semester = models.ForeignKey(
        'Semester',
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )
    image = OptimizedImageField(
        upload_to=get_report_path,
        optimized_image_resize_method='thumbnail',
        null=True,
        blank=True,
    )
    link = models.URLField(
        max_length=100,
        null=True,
        blank=True,
    )
    hours = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
    )
    uploaded = models.DateTimeField(
        auto_now_add=True,
        null=False
    )
    approval = models.BooleanField(
        null=True
    )

    class Meta:
        db_table = "self_sport_report"
        constraints = [
            models.CheckConstraint(
                name="link_xor_image",
                check=models.Q(
                    link__isnull=False,
                    image__isnull=True,
                ) | models.Q(
                    link__isnull=True,
                    image__isnull=False,
                )
            )
        ]

    def save(self, *args, **kwargs):
        # update flag and approval only when object is created via API
        if not kwargs.get('force_insert', False):
            self.hours = max(self.hours, 0)
            self.approval = self.hours > 0
        return super().save(*args, **kwargs)
