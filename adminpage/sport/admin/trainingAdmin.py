from django.contrib import admin

from sport.models import Training
from .inlines import AttendanceInline
from .utils import cache_filter, cache_dependent_filter, cache_alternative_filter


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
        # semester filter, resets group sub filter
        (
            "group__semester",
            cache_filter(admin.RelatedFieldListFilter, ["group__id"])
        ),
        # group filter, depends on chosen semester
        (
            "group",
            cache_dependent_filter({"group__semester": "semester"})
        ),
        ("training_class", admin.RelatedOnlyFieldListFilter),
        ("start", cache_alternative_filter(admin.DateFieldListFilter, ["group__semester"])),
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
