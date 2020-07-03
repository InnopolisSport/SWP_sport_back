from django.contrib import admin

from sport.models import MedicalGroup
from .site import site


@admin.register(MedicalGroup, site=site)
class MedicalGroupAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    fields = ("name", "description")

    def has_add_permission(self, request):
        return False
