from admin_auto_filters.filters import AutocompleteFilter
from django.contrib import admin

from sport.models import Group
from .inlines import ScheduleInline, EnrollInline, TrainingInline
from .utils import custom_titled_filter
from .site import site


class TrainerTextFilter(AutocompleteFilter):
    title = "trainer"
    field_name = "trainer"


@admin.register(Group, site=site)
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

    class Media:
        pass
