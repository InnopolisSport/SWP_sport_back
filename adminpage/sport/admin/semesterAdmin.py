from django.contrib import admin

from sport.models import Semester


@admin.register(Semester)
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
        "choice_deadline",
    )
