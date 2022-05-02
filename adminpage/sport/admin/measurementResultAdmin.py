from django.contrib import admin

from api.crud import get_ongoing_semester
from sport.models import FitnessTestExercise, FitnessTestGrading

from .site import site


class MeasurementResult(admin.ModelAdmin):
    list_display = (
        "session",
        "measurement",
        "value"
    )
