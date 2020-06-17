from django.contrib import admin

from sport.models import Sport
from .site import site


@admin.register(Sport, site=site)
class SportAdmin(admin.ModelAdmin):
    search_fields = (
        "name",
    )

    list_display = (
        "name",
        "special",
    )

    list_filter = (
        "special",
    )
    # maybe it will be inconvenient
    # inlines = (
    #     GroupInline,
    # )
