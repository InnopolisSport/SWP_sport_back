from django.contrib import admin

from sport.models import Training


@admin.register(Training)
class TrainingAdmin(admin.ModelAdmin):
    list_filter = (
        "group__semester",
        ("group", admin.RelatedOnlyFieldListFilter),
        ("training_class", admin.RelatedOnlyFieldListFilter),
        "start",
    )

    list_display = (
        "group",
        # "schedule",
        "start",
        "end",
        "training_class",
    )
