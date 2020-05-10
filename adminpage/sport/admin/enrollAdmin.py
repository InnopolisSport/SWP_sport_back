from django.contrib import admin

from .fabrics import semester_filter_fabric
from .mixins import EnrollExportXlsxMixin


class EnrollAdmin(admin.ModelAdmin, EnrollExportXlsxMixin):
    list_filter = [semester_filter_fabric("group__semester__id")]
    actions = ["export_as_csv"]
