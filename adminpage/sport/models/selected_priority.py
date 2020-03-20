from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class SelectedPriority(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, null=False)
    group = models.ForeignKey("Group", on_delete=models.CASCADE, null=False)
    priority = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], null=False)
    quiz = models.ForeignKey('Quiz', on_delete=models.CASCADE, null=False)

    class Meta:
        db_table = "selected_priority"
        constraints = [
            models.UniqueConstraint(fields=["user_id", "group_id", "quiz_id"], name="unique_priority_vote")
        ]

    def __str__(self):
        return f"{self.user.email} {self.group.name}-{self.priority}"
