from django.db import models


class Sport(models.Model):
    name = models.CharField(max_length=50, null=False)
    special = models.BooleanField(default=False, null=False, verbose_name="Technical/Club only")

    class Meta:
        db_table = "sport"
        verbose_name = "sport type"
        verbose_name_plural = "sport types"
        indexes = [
            models.Index(fields=("name",)),
        ]
        permissions = [
            ('choose_sport', "Can choose type of sport"),
            ("go_to_another_sport", "Can got to group of the another type of sport")
        ]

    def __str__(self):
        return f"{self.name}"
