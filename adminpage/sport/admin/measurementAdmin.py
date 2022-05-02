from django.contrib import admin
from .site import site


class Measurement(admin.ModelAdmin):
    list_display = (
        "name",
        "value_unit"
    )
