from admin_auto_filters.filters import AutocompleteFilter
from django.contrib import admin

from sport.models import Group
from .inlines import ScheduleInline, EnrollInline, TrainingInline
from .utils import custom_titled_filter, cache_dependent_filter, cache_filter


class TrainerTextFilter(AutocompleteFilter):
    title = "trainer"
    field_name = "trainer"


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    search_fields = (
        "name",
    )

    autocomplete_fields = (
        "sport",
        "trainer",
    )

    list_filter = (
        ("semester", admin.RelatedOnlyFieldListFilter),
        ("is_club", custom_titled_filter("club status")),
        TrainerTextFilter,
        ("sport", admin.RelatedOnlyFieldListFilter),
    )

    list_display = (
        "__str__",
        "sport",
        "is_club",
        "trainer",
    )

    inlines = (
        ScheduleInline,
        TrainingInline,
        EnrollInline,
    )

    def lookup_allowed(self, key, value):
        if key in ('semester__start__year',):
            return True
        return super().lookup_allowed(key, value)

    class Media:
        pass
