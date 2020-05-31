from django.contrib import admin

from sport.models import Group
from .inlines import ScheduleInline, EnrollInline, TrainingInline


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
        "name",
        "semester",
        "is_club",
        ("sport", admin.RelatedOnlyFieldListFilter),
        ("trainer", admin.RelatedOnlyFieldListFilter),
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
        js = (
            "sport/js/list_filter_collapse.js",
        )
