from admin_auto_filters.filters import AutocompleteFilter
from django.contrib import admin

from sport.admin.utils import year_filter, cache_filter, cache_dependent_filter
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
        # filter on study year, resets semester and group sub filters
        cache_filter(year_filter("training__start__year"), ["training__group__semester__id", "training__group__id"]),
        # semester filter, depends on chosen year, resets group sub filter
        (
            "training__group__semester",
            cache_filter(cache_dependent_filter({"training__start__year": "start__year"}), ["training__group__id"])
        ),
        # group filter, depends on chosen year and semester
        (
            "training__group",
            cache_dependent_filter({
                "training__group__semester": "semester__pk",
                "training__start__year": "semester__start__year"
            })
        ),
        StudentTextFilter,
        "training__start",
    )

    class Media:
        js = (
            "sport/js/list_filter_collapse.js",
        )
