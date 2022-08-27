from django.contrib import admin

from training_suggestor.admin.site import site
from training_suggestor.models import SportType


@admin.register(SportType, site=site)
class SportTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
