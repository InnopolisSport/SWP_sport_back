from django.contrib import admin

from sport.models import Schedule


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_filter = (
        "group__semester",
        ("group", admin.RelatedOnlyFieldListFilter),
        "weekday",
        "start",
        ("training_class", admin.RelatedOnlyFieldListFilter)
    )

    list_display = (
        "group",
        "weekday",
        "start",
        "end",
        "training_class",
    )

    class Media:
        js = (
            "sport/js/list_filter_collapse.js",
        )
