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
    )
