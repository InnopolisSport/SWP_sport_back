from django.contrib import admin

from sport.models import Trainer


@admin.register(Trainer)
class TrainerAdmin(admin.ModelAdmin):
    search_fields = (
        "user__first_name",
        "user__last_name",
        "user__email"
    )

    list_display = (
        "__str__",
        "user",
    )
