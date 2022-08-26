from django.contrib import admin

from training_suggestor.admin.site import site
from training_suggestor.models import Exercise


@admin.register(Exercise, site=site)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'power_zone',
        'repeat',
        'set',
        'rest_interval'
    )
