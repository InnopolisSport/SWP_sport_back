from django.contrib import admin
from import_export import resources, fields
from import_export.admin import ImportMixin
from import_export.widgets import ForeignKeyWidget

from training_suggestor.admin.site import site
from training_suggestor.admin.utils.import_export import CommaFloatWidget, SecondsDurationWidget
from training_suggestor.models import ExerciseParams, PowerZone, Exercise, SportType


class ExerciseResource(resources.ModelResource):
    power_zone = fields.Field(column_name='power_zone', attribute='power_zone', widget=ForeignKeyWidget(PowerZone, 'number'))
    exercise = fields.Field(column_name='exercise', attribute='exercise', widget=ForeignKeyWidget(Exercise, 'name'))
    sport = fields.Field(column_name='sport', attribute='sport', widget=ForeignKeyWidget(SportType, 'name'))

    WIDGETS_MAP = {
        'FloatField': CommaFloatWidget,
        'DurationField': SecondsDurationWidget,
    }

    class Meta:
        model = ExerciseParams
        import_id_fields = ()
        fields = ('exercise', 'type', 'sport', 'power_zone', 'repeat', 'set', 'rest_interval')


@admin.register(ExerciseParams, site=site)
class ExerciseParamsAdmin(ImportMixin, admin.ModelAdmin):
    resource_class = ExerciseResource
    list_display = ('exercise', 'type', 'sport', 'power_zone', 'repeat', 'set', 'rest_interval')
