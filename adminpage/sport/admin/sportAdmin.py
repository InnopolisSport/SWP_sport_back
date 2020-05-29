from django.contrib import admin

from sport.models import Sport


@admin.register(Sport)
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
