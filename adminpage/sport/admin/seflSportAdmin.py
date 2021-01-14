from admin_auto_filters.filters import AutocompleteFilter
from django.contrib import admin
from django.db.models import F
from django.utils.html import format_html

from sport.models import SelfSportReport
from .site import site
from .utils import custom_order_filter


class StudentTextFilter(AutocompleteFilter):
    title = "student"
    field_name = "student"


@admin.register(SelfSportReport, site=site)
class SelfSportAdmin(admin.ModelAdmin):
    list_display = (
        'student',
        'semester',
        'link',
        'image',
        'hours',
        'uploaded',
        'approval'
    )

    list_filter = (
        StudentTextFilter,
        ("semester", custom_order_filter(("-start",))),
        "approval"
    )

    fields = (
        "student",
        "semester",
        "uploaded",
        "hours",
        "link",
        "reference_image",
    )

    readonly_fields = (
        "uploaded",
        "reference_image",
    )

    autocomplete_fields = (
        "student",
    )

    def reference_image(self, obj):
        if obj.image is not None:
            return format_html(
                '<a href="{}"><img style="width: 50%" src="{}" /></a>',
                obj.image.url,
                obj.image.url
            )
        else:
            return "None"

    reference_image.short_description = 'Reference'
    reference_image.allow_tags = True

    ordering = (F("approval").asc(nulls_first=True), "uploaded")

    class Media:
        pass
