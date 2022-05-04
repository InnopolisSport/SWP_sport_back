from django.contrib import admin
from .site import site
from sport.models import MeasurementSession, MeasurementResult
from api.crud.crud_semester import get_ongoing_semester


class MeasurementResultInline(admin.TabularInline):
    model = MeasurementResult

    fields = ("measurement", "value")
    readonly_fields = ("measurement", )


    extra = 0

    def has_add_permission(self, request, obj):
        return False

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'semester':
            kwargs['initial'] = get_ongoing_semester()
            return db_field.formfield(**kwargs)
        return super().formfield_for_foreignkey(
            db_field, request, **kwargs
        )


class AddMeasurementResultInline(MeasurementResultInline):
    extra = 4
    readonly_fields = ()



    def has_view_or_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj):
        return True

@admin.register(MeasurementSession, site=site)
class MeasurementSession(admin.ModelAdmin):
    list_display = (
        "student",
        "date",
        "semester",
        "approved"
    )

    inlines = (MeasurementResultInline, AddMeasurementResultInline)

