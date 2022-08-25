from django.contrib import admin
from django.forms import ModelForm, CheckboxSelectMultiple

from sport.models import Semester
from .site import site


class SemesterAdminForm(ModelForm):
    class Meta:
        model = Semester
        fields = '__all__'  # will be overridden by ModelAdmin
        widgets = {
            'nullify_groups': CheckboxSelectMultiple(),
            'participating_courses': CheckboxSelectMultiple()
        }


@admin.register(Semester, site=site)
class SemesterAdmin(admin.ModelAdmin):
    form = SemesterAdminForm
    search_fields = (
        "name",
        "start",
    )

    ordering = (
        "-start",
    )
    list_display = (
        "name",
        "start",
        "end",
        "hours",
        "points_fitness_test",
    )

    def get_fields(self, request, obj=None):
        if obj is None:
            return (
                "name",
                "start",
                "end",
                "hours",
                "points_fitness_test",
                "academic_leave_students",
                "participating_courses",
                "number_hours_one_week_ill",
                "nullify_groups",
                "increase_course"
            )
        return (
            "name",
            "start",
            "end",
            "hours",
            "points_fitness_test",
            "academic_leave_students",
            "number_hours_one_week_ill",
            "participating_courses",
        )

    autocomplete_fields = ('academic_leave_students',)
