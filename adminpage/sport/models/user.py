from django.core.validators import RegexValidator
from django.db import models

# Create your models here.
course_id_validator = RegexValidator(r"^[A-Z]{1,2}\d{2}(-[A-Z]{2}-\d{2})?$", "Accepts: B18 B17-SB, etc")


class User(models.Model):
    class UserType(models.IntegerChoices):
        STUDENT = 0, "Student"
        TRAINER = 1, "Trainer"
        STUDENT_CLUB_LEADER = 2, "Student+ClubLeader"
        ADMIN = 3, "Admin"

    first_name = models.CharField(max_length=25, null=False)
    last_name = models.CharField(max_length=25, null=False)
    email = models.CharField(max_length=100, null=False, unique=True)
    type = models.IntegerField(choices=UserType.choices, default=UserType.STUDENT)
    course_id = models.CharField(max_length=6)

    class Meta:
        db_table = "user"
        verbose_name_plural = "users"

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.get_type_display()}"
