from django.contrib import admin

from .models import Exercise
from .site import site


@admin.register(Exercise, site=site)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'power_zone',
        'repeat',
        'set',
        'rest_interval'
    )
