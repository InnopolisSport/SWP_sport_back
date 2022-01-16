from django.db import models

from sport.models.enums import GroupQR


class Group(models.Model):
    name = models.CharField(max_length=50, null=False)
    description = models.CharField(max_length=1000, null=True, blank=True)
    link_name = models.CharField(max_length=100, null=True, blank=True)
    link = models.URLField(max_length=256, null=True, blank=True)
    capacity = models.PositiveIntegerField(default=50, null=False)
    is_club = models.BooleanField(default=False, null=False)
    sport = models.ForeignKey('Sport', on_delete=models.CASCADE, null=True, blank=True)
    semester = models.ForeignKey('Semester', on_delete=models.CASCADE, null=False)
    trainer = models.ForeignKey('Trainer', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='teacher')
    trainers = models.ManyToManyField('Trainer', related_name='m2m', blank=True, verbose_name='teachers')

    # minimum_medical_group = models.ForeignKey('MedicalGroup', on_delete=models.DO_NOTHING, null=True, blank=True)
    allowed_medical_groups = models.ManyToManyField('MedicalGroup', blank=True)
    allowed_qr = models.IntegerField(
        choices=GroupQR.choices,
        default=-1,
        verbose_name="Is a QR required?"
    )

    class Meta:
        db_table = "group"
        verbose_name_plural = "groups"
        indexes = [
            models.Index(fields=("name",)),
        ]

    def __str__(self):
        return f"[{self.semester}] {f'{self.sport} - ' if self.sport is not None else ''}{self.name}"
