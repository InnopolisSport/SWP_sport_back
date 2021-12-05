from django.contrib import admin
from sport.models import FitnessTestExercise

from .site import site


@admin.register(FitnessTestExercise, site=site)
class FitnessTestExerciseAdmin(admin.ModelAdmin):
    list_display = (
        'exercise_name',
        'value_unit',
    )
