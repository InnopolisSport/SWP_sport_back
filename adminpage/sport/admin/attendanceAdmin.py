from admin_auto_filters.filters import AutocompleteFilter
from django.contrib import admin

from sport.models import Attendance


class StudentTextFilter(AutocompleteFilter):
    title = "student"
    field_name = "student"


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
        StudentTextFilter,
        "training__start",
    )

    class Media:
        js = (
            "sport/js/list_filter_collapse.js",
        )
