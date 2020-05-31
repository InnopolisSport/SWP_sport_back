from django.contrib import admin

from sport.models import Training
from .inlines import AttendanceInline


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
        "group__semester",
        ("group", admin.RelatedOnlyFieldListFilter),
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
