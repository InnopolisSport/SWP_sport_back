from django.contrib import admin

from sport.models import Sport


@admin.register(Sport)
class SportAdmin(admin.ModelAdmin):
    save_on_top = True
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
