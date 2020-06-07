from django.contrib import admin

from sport.models import Semester
from .utils import year_filter


@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    search_fields = (
        "name",
        "start",
    )

    ordering = (
        "-start",
    )

    list_filter = (
        year_filter(Semester, 'start__year'),
    )

    list_display = (
        "name",
        "start",
        "end",
        "choice_deadline",
    )
