from django.contrib import admin
from .site import site
from sport.models import MeasurementSession


@admin.register(MeasurementSession, site=site)
class MeasurementSession(admin.ModelAdmin):
    list_display = (
        "student",
        "date",
        "semester",
        "approved"
    )
