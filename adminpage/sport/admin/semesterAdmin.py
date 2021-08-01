from django.contrib import admin

from sport.models import Semester
from .site import site


@admin.register(Semester, site=site)
class SemesterAdmin(admin.ModelAdmin):
    search_fields = (
        "name",
        "start",
    )

    ordering = (
        "-start",
    )
    list_display = (
        "name",
        "start",
        "end",
        "hours",
        "academic_students"
    )

    filter_horizontal = ('academic_leave_students',)

    def academic_students(self, obj):
        return "\n".join([p.user.email for p in obj.academic_leave_students.all()])
