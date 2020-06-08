from django.contrib import admin

from sport.models import Schedule
from .inlines import ViewTrainingInline
from .utils import cache_filter, year_filter, cache_dependent_filter


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    autocomplete_fields = (
        "group",
        "training_class"
    )

    search_fields = (
        "group__name",
    )

    ordering = (
        "start",
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
        "weekday",
        "start",
        ("training_class", admin.RelatedOnlyFieldListFilter)
    )

    list_display = (
        "group",
        "weekday",
        "start",
        "end",
        "training_class",
    )

    inlines = (
        ViewTrainingInline,
    )

    def lookup_allowed(self, key, value):
        if key in ('group__semester__start__year',):
            return True
        return super().lookup_allowed(key, value)

    def get_readonly_fields(self, request, obj=None):
        """
        Make some-fields immutable once set
        """
        if obj is not None:
            return self.readonly_fields + ('group',)
        return self.readonly_fields

    class Media:
        js = (
            "sport/js/list_filter_collapse.js",
        )
