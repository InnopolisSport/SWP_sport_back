from admin_auto_filters.filters import AutocompleteFilter
from django import forms
from django.contrib import admin
from django.utils.html import format_html

from sport.admin import site
from sport.models import MedicalGroupReference, MedicalGroup


class StudentTextFilter(AutocompleteFilter):
    title = "student"
    field_name = "student"


class MedicalGroupReferenceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.student_id is not None:
            self.fields['medical_group'].initial = self.instance.student.medical_group_id

    medical_group = forms.ModelChoiceField(MedicalGroup.objects.all(), initial=-2)

    def save(self, commit=True):
        instance = super().save(commit)
        instance.student.medical_group_id = self.cleaned_data['medical_group'].pk
        instance.student.save()
        return instance

    class Meta:
        model = MedicalGroupReference
        fields = (
            'student',
        )


@admin.register(MedicalGroupReference, site=site)
class MedicalGroupReferenceAdmin(admin.ModelAdmin):
    form = MedicalGroupReferenceForm
    list_display = (
        "student",
        "image",
        "resolved",
    )

    list_select_related = (
        "student",
        "student__user",
    )

    list_filter = (
        "resolved",
        StudentTextFilter,
    )

    fields = (
        "student",
        "medical_group",
        "reference_image",
    )

    readonly_fields = (
        "student",
        "reference_image",
    )

    def has_add_permission(self, request):
        return False

    def reference_image(self, obj):
        return format_html('<a href="{}"><img style="width: 50%" src="{}" /></a>', obj.image.url, obj.image.url)

    reference_image.short_description = 'Reference'
    reference_image.allow_tags = True

    class Media:
        pass
