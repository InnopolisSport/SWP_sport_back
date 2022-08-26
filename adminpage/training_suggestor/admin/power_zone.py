from django.contrib import admin
from import_export import resources
from import_export.admin import ImportMixin

from training_suggestor.admin.site import site
from training_suggestor.admin.utils.import_export import CommaFloatWidget
from training_suggestor.models import PowerZone


class PowerZoneResource(resources.ModelResource):
    WIDGETS_MAP = {
        'FloatField': CommaFloatWidget,
    }

    class Meta:
        model = PowerZone
        import_id_fields = ('number',)
        fields = ('number', 'description', 'pulse', 'ratio')


@admin.register(PowerZone, site=site)
class PowerZoneAdmin(ImportMixin, admin.ModelAdmin):
    resource_class = PowerZoneResource
    list_display = ('number', 'description', 'pulse', 'ratio')
    ordering = ('number',)
