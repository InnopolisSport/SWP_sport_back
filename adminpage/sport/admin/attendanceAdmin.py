from django.contrib import admin

from sport.models import Attendance


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "training",
        "hours",
    )

    list_filter = (
        "training__group__semester",
        ("training__group", admin.RelatedOnlyFieldListFilter),
        ("student", admin.RelatedOnlyFieldListFilter),
        "training__start",
    )

    class Media:
        js = (
            "sport/js/list_filter_collapse.js",
        )
