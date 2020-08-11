from admin_auto_filters.filters import AutocompleteFilter
from django.contrib import admin
from django.utils.html import format_html

from sport.admin import site
from sport.models import MedicalGroupReference


class StudentTextFilter(AutocompleteFilter):
    title = "student"
    field_name = "student"


@admin.register(MedicalGroupReference, site=site)
class MedicalGroupReferenceAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "image",
        "resolved",
    )

    list_select_related = (
        "student",
        "student__user",
    )

    autocomplete_fields = (
        "student",
    )

    list_filter = (
        "resolved",
        StudentTextFilter,
    )

    fields = (
        "student",
        "student__medical_group",
        "reference_image",
    )

    readonly_fields = (
        "reference_image",
    )

    def reference_image(self, obj):
        return format_html('<a href="{}"><img style="width: 50%" src="{}" /></a>', obj.image.url, obj.image.url)

    reference_image.short_description = 'Reference'
    reference_image.allow_tags = True

    class Media:
        pass
