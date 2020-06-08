from django.contrib import admin

from sport.models import Schedule
from .inlines import ViewTrainingInline
from .utils import cache_filter, cache_dependent_filter


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
