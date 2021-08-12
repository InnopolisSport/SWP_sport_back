from django.contrib import admin
from django.forms import ModelForm, CheckboxSelectMultiple

from sport.models import Semester
from .site import site
from ..models import Group


class SemesterAdminForm(ModelForm):
    class Meta:
        model = Semester
        fields = '__all__'  # will be overridden by ModelAdmin
        widgets = {
            'nullify_groups': CheckboxSelectMultiple()
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
    )

    fields = (
        "name",
        "start",
        "end",
        "hours",
        "academic_leave_students",
        "number_hours_one_week_ill",
        "nullify_groups",
        "increase_course"
    )

    filter_horizontal = ('academic_leave_students',)

