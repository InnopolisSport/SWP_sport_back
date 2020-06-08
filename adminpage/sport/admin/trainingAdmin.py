from django.contrib import admin

from sport.models import Training
from .inlines import AttendanceInline
from .utils import cache_filter, year_filter, cache_dependent_filter


@admin.register(Training)
class TrainingAdmin(admin.ModelAdmin):
    search_fields = (
        "group__name",
    )

    autocomplete_fields = (
        "group",
        "schedule",
        "training_class",
    )

    ordering = (
        'start',
    )

    list_filter = (
        # filter on study year, resets semester and group sub filters
        cache_filter(year_filter("group__semester__start__year"), ["group__semester__id", "group__id"]),
        # semester filter, depends on chosen year, resets group sub filter
        (
            "group__semester",
            cache_filter(cache_dependent_filter({"group__semester__start__year": "start__year"}), ["group__id"])
        ),
        # group filter, depends on chosen year and semester
        (
            "group",
            cache_dependent_filter({
                "group__semester__start__year": "semester__start__year",
                "group__semester": "semester"
            })
        ),
        ("training_class", admin.RelatedOnlyFieldListFilter),
        "start",
    )

    list_display = (
        "group",
        # "schedule",
        "start",
        "end",
        "training_class",
    )

    inlines = (
        AttendanceInline,
    )

    def lookup_allowed(self, key, value):
        if key in ('group__semester__start__year',):
            return True
        return super().lookup_allowed(key, value)
