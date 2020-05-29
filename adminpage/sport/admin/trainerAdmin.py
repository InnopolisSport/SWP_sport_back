from django.contrib import admin

from sport.models import Trainer


@admin.register(Trainer)
class TrainerAdmin(admin.ModelAdmin):
    search_fields = (
        "first_name",
        "last_name",
    )

    list_display = (
        "__str__",
        "email",
    )
