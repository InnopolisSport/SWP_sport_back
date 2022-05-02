from django.contrib import admin
from .site import site


class MeasurementSession(admin.ModelAdmin):
    list_display = (
        "student",
        "date",
        "semester",
        "approved"
    )
