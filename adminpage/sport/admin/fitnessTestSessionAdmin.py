from django.contrib import admin

from api.crud import get_ongoing_semester
from sport.models import FitnessTestSession, FitnessTestResult

from .site import site

class FitnessTestResultInline(admin.TabularInline):
    model = FitnessTestResult

    autocomplete_fields = ("student", )

    extra = 0

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        print(db_field.name)
        if db_field.name == 'semester':
            kwargs['initial'] = get_ongoing_semester()
            return db_field.formfield(**kwargs)
        return super().formfield_for_foreignkey(
            db_field, request, **kwargs
        )


@admin.register(FitnessTestSession, site=site)
class FitnessTestSessionAdmin(admin.ModelAdmin):
    autocomplete_fields = (
        "teacher",
    )

    list_display = (
        'date',
        'teacher',
    )

    inlines = (FitnessTestResultInline,)
