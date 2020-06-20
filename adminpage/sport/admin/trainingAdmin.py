from django.conf import settings
from django.contrib import admin
from django import forms
from django.contrib.admin.widgets import AutocompleteSelectMultiple
from django.db import transaction
from django.http import HttpResponseRedirect
from django.utils import timezone

from api.crud import get_ongoing_semester
from sport.models import Training, Student, Attendance, Group
from .inlines import AttendanceInline
from .utils import cache_filter, cache_dependent_filter, cache_alternative_filter, custom_order_filter
from .site import site


class AutocompleteStudent:
    model = Student


class CreateTrainingForm(forms.ModelForm):
    attended_students = forms.ModelMultipleChoiceField(
        queryset=Student.objects.all(),
        widget=AutocompleteSelectMultiple(
            rel=AutocompleteStudent,
            admin_site=site,
            attrs={'data-width': '50%'}
        )
    )
    hours = forms.DecimalField(max_digits=5, decimal_places=2, min_value=0.01, max_value=999.99, initial=1)

    @transaction.atomic
    def save(self, commit=True):
        training = super().save()
        if not commit:
            self.save_m2m = lambda: None
        for student in self.cleaned_data['attended_students']:
            Attendance.objects.create(student=student, training=training, hours=self.cleaned_data['hours'])
        return training

    class Meta:
        model = Training
        fields = ('group', 'start', 'end')
CreateTrainingForm.title = "Add extra training"


@admin.register(Training, site=site)
class TrainingAdmin(admin.ModelAdmin):
    search_fields = (
        "group__name",
    )

    autocomplete_fields = (
        "group",
        "schedule",
        "training_class",
    )

    ordering = (
        '-start',
    )

    list_filter = (
        # semester filter, resets group sub filter
        (
            "group__semester",
            cache_filter(custom_order_filter(("-start",)), ["group__id"])
        ),
        # group filter, depends on chosen semester
        (
            "group",
            cache_dependent_filter({"group__semester": "semester"}, ("name",))
        ),
        ("training_class", admin.RelatedOnlyFieldListFilter),
        ("start", cache_alternative_filter(admin.DateFieldListFilter, ["group__semester"])),
    )

    list_display = (
        "group",
        # "schedule",
        "start",
        "end",
        "training_class",
    )

    inlines = (
        AttendanceInline,
    )

    def response_add(self, request, obj, post_url_continue=None):
        res = super().response_add(request, obj, post_url_continue)
        if "_addanother" in request.POST:
            redirect_url = request.path + ('?extra=' if 'extra' in request.GET else '')
            return HttpResponseRedirect(redirect_url)
        else:
            return res

    def get_form(self, request, obj=None, change=False, **kwargs):
        if 'extra' in request.GET:
            kwargs['form'] = CreateTrainingForm
        return super().get_form(request, obj, change, **kwargs)

    def get_formsets_with_inlines(self, request, obj=None):
        if 'extra' not in request.GET:
            yield from super().get_formsets_with_inlines(request, obj)

    def get_changeform_initial_data(self, request):
        if 'extra' in request.GET:
            return {
                "group": Group.objects.get(semester=get_ongoing_semester(), name=settings.EXTRA_EVENTS_GROUP_NAME),
                "start": timezone.now().replace(minute=0, second=0),
                "end": timezone.now().replace(minute=30, second=0),
            }
        return {}
