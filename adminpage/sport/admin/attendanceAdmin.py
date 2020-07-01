from admin_auto_filters.filters import AutocompleteFilter
from django.contrib import admin

from sport.admin.utils import cache_filter, cache_dependent_filter, cache_alternative_filter, custom_order_filter
from sport.models import Attendance
from .site import site


class StudentTextFilter(AutocompleteFilter):
    title = "student"
    field_name = "student"


@admin.register(Attendance, site=site)
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

    ordering = (
        "-training__start",
    )

    list_filter = (
        StudentTextFilter,
        # semester filter, resets group sub filter
        (
            "training__group__semester",
            cache_filter(custom_order_filter(("-start",)), ["training__group__id"])
        ),
        # group filter, depends on chosen semester
        (
            "training__group",
            cache_dependent_filter({"training__group__semester": "semester__pk"}, ("name",), select_related=["semester"])
        ),
        ("training__start", cache_alternative_filter(admin.DateFieldListFilter, ["training__group__semester"])),
    )

    list_select_related = (
        "student__user",
        "training__group",
        "training__group__semester",
        "training__training_class",
    )

    class Media:
        pass
