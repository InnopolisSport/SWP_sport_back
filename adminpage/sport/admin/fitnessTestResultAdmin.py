from django.contrib import admin
from sport.models import FitnessTestResult

from .site import site


@admin.register(FitnessTestResult, site=site)
class FitnessTestResultAdmin(admin.ModelAdmin):
    autocomplete_fields = (
        "student",
    )

    list_display = (
        'student',
        'exercise',
        'semester',
        'value',
    )

    def has_add_permission(self, request, obj=None):
        return False
