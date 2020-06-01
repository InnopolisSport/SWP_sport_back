from django.contrib import admin

from sport.models import Enroll

from .mixins import EnrollExportXlsxMixin
from .utils import custom_titled_filter


@admin.register(Enroll)
class EnrollAdmin(admin.ModelAdmin, EnrollExportXlsxMixin):
    autocomplete_fields = (
        "student",
        "group",
    )

    list_filter = (
        "group__semester",
        ("group", admin.RelatedOnlyFieldListFilter),
        ("group__is_club", custom_titled_filter("club status")),
        ("is_primary", custom_titled_filter("primary status")),
        ("group__sport", admin.RelatedOnlyFieldListFilter),
        ("group__trainer", admin.RelatedOnlyFieldListFilter),

    )
    list_display = (
        'student',
        'group',
        'is_primary',
    )
    actions = (
        "export_as_csv",
    )

    class Media:
        js = (
            "sport/js/list_filter_collapse.js",
        )
