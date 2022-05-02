from django.contrib import admin

from sport.models import MeasurementResult


from .site import site


@admin.register(MeasurementResult, site=site)
class MeasurementResult(admin.ModelAdmin):
    list_display = (
        "session",
        "measurement",
        "value"
    )
