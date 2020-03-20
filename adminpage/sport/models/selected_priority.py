from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class SelectedPriority(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, null=False)
    group = models.ForeignKey("Group", on_delete=models.CASCADE, null=False)
    priority = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], null=False)
    quiz = models.ForeignKey('Quiz', on_delete=models.CASCADE, null=False)

    class Meta:
        db_table = "selected_priority"
        verbose_name_plural = "selected priorities"
        constraints = [
            models.UniqueConstraint(fields=["user_id", "group_id", "quiz_id"], name="unique_priority_vote")
        ]

    def __str__(self):
        return f"{self.user.email} {self.group.name}-{self.priority}"
