from django.contrib import admin
from import_export.admin import ImportMixin

from training_suggestor.admin.site import site
from training_suggestor.models import Exercise


@admin.register(Exercise, site=site)
class ExerciseAdmin(ImportMixin, admin.ModelAdmin):
    pass
    # list_display = (
    #     'name',
    #     'power_zone',
    #     'repeat',
    #     'set',
    #     'rest_interval'
    # )
