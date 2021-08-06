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
    )

    fields = (
        "name",
        "start",
        "end",
        "hours",
        "academic_leave_students",
        "number_hours_one_week_ill",
    )

    filter_horizontal = ('academic_leave_students',)

