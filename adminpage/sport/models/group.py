from django.db import models


class Group(models.Model):
    name = models.CharField(max_length=50, null=False)
    sport_id = models.ForeignKey('Sport', on_delete=models.CASCADE)
    trainer_id = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = "group"

    def __str__(self):
        return f"{self.name}"
