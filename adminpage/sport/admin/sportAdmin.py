from django.contrib import admin

from sport.models import Sport


@admin.register(Sport)
class SportAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "special",
    )

    list_filter = (
        "special",
    )
