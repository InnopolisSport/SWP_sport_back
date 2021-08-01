from django.db import models

from sport.models import Group


class Sport(models.Model):
    name = models.CharField(max_length=50, null=False)
    special = models.BooleanField(default=False, null=False, verbose_name="Technical/Club only")

    @property
    def trainers(self):
        t = []
        for group in Group.objects.filter(sport=self):
            if group.trainer:
                t.append(group.trainer)
        return t

    @property
    def groups(self):
        return Group.objects.filter(sport=self)

    class Meta:
        db_table = "sport"
        verbose_name = "sport type"
        verbose_name_plural = "sport types"
        indexes = [
            models.Index(fields=("name",)),
        ]

    def __str__(self):
        return f"{self.name}"
