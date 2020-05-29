from django.contrib import admin

from sport.models import Attendance


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    # TODO: test performance
    # https://docs.djangoproject.com/en/3.0/ref/contrib/admin/#django.contrib.admin.ModelAdmin.autocomplete_fields
    autocomplete_fields = (
        "training",
        "student",
    )

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
