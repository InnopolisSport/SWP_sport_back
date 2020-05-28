from django.contrib import admin

from sport.models import Enroll

from .fabrics import semester_filter_fabric
from .mixins import EnrollExportXlsxMixin
from .utils import custom_titled_filter


@admin.register(Enroll)
class EnrollAdmin(admin.ModelAdmin, EnrollExportXlsxMixin):
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