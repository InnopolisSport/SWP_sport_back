from django.contrib import admin
from import_export import resources
from import_export.admin import ImportMixin

from training_suggestor.admin.site import site
from training_suggestor.admin.utils.import_export import CommaFloatWidget, SecondsDurationWidget
from training_suggestor.models import Exercise


class ExerciseResource(resources.ModelResource):
    WIDGETS_MAP = {
        'FloatField': CommaFloatWidget,
        'DurationField': SecondsDurationWidget,
    }

    class Meta:
        model = Exercise
        import_id_fields = ()
        fields = ('name', 'ratio', 'avg_time')


@admin.register(Exercise, site=site)
class ExerciseAdmin(ImportMixin, admin.ModelAdmin):
    resource_class = ExerciseResource
    list_display = ('name', 'description', 'ratio', 'avg_time')
