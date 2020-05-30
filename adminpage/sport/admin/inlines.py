from django.contrib import admin
from django.http import HttpRequest

from sport import models
from .utils import get_inline

AttendanceInline = get_inline(
    models.Attendance,
    extra=1,
    autocomplete_fields=("training", "student"),
)
ScheduleInline = get_inline(
    models.Schedule,
    extra=1,
)
EnrollInline = get_inline(
    models.Enroll,
    extra=1,
    autocomplete_fields=("student",),
)
GroupInline = get_inline(models.Group,
                         extra=0,
                         )


class TrainingInline(admin.TabularInline):
    model = models.Training
    autocomplete_fields = ("training_class",)
    extra = 1


class ViewTrainingInline(TrainingInline):
    exclude = ("group",)
    extra = 0

    def has_add_permission(
            self, request: HttpRequest, *args, **kwargs
    ) -> bool:
        return False
