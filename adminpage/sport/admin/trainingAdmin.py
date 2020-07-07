import csv
import io
from collections import OrderedDict

from django.conf import settings
from django.contrib import admin
from django import forms
from django.contrib.admin.widgets import AutocompleteSelectMultiple
from django.db import transaction
from django.http import HttpResponseRedirect
from django.utils import timezone

from api.crud import get_ongoing_semester, mark_hours
from sport.models import Training, Student, Group
from .inlines import ViewAttendanceInline, AddAttendanceInline
from .utils import cache_filter, cache_dependent_filter, cache_alternative_filter, custom_order_filter
from .site import site


class AutocompleteStudent:
    model = Student


class TrainingFormWithCSV(forms.ModelForm):
    attended_students = forms.ModelMultipleChoiceField(
        required=False,
        queryset=Student.objects.all(),
        widget=AutocompleteSelectMultiple(
            rel=AutocompleteStudent,
            admin_site=site,
            attrs={'data-width': '50%'}
        )
    )
    hours = forms.DecimalField(required=False, max_digits=5, decimal_places=2, min_value=0.01, max_value=999.99,
                               initial=1)
    csv = forms.FileField(required=False, widget=forms.FileInput(attrs={'accept': '.csv'}))

    def clean(self):
        cleaned_data = super().clean()
        attendances = []
        cleaned_data['attendances'] = attendances
        file = cleaned_data.get("csv", None)
        if file is None:
            return cleaned_data
        data = file.read().decode('UTF-8')
        emails = []
        hours = {}
        for row in csv.reader(io.StringIO(data)):
            if len(row) != 2:
                raise forms.ValidationError(f"Expected 2 columns in each row, got {row}")
            emails.append(row[0])
            try:
                hours[row[0]] = round(float(row[1]), 2)
                assert 0 <= hours[row[0]] < 1000
            except:
                raise forms.ValidationError(
                    f"Got invalid hours value \"{row[1]}\" for email {row[0]}, expected value in range [0,999.99]")
        students = Student.objects.select_related('user').filter(user__email__in=emails)
        if len(students) != len(emails):
            missing = set(emails) - set(map(lambda student: student.user.email, students))
            raise forms.ValidationError(
                f"File contains {len(emails)} records. Only {len(students)} emails matched. "
                f"Missing students emails are: {', '.join(missing)}"
            )

        for student in students:
            attendances.append((student, hours[student.user.email]))


class ChangeTrainingForm(TrainingFormWithCSV):
    class Meta:
        model = Training
        fields = ('group', 'schedule', 'start', 'end', 'training_class')


class CreateExtraTrainingForm(TrainingFormWithCSV):
    class Meta:
        model = Training
        fields = ('group', 'start', 'end')


CreateExtraTrainingForm.title = "Add extra training"


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
            cache_dependent_filter({"group__semester": "semester"}, ("name",), select_related=["semester"])
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

    fields = (
        "group",
        "schedule",
        "start",
        "end",
        "training_class",
    )

    list_select_related = (
        "group__semester",
        "training_class",
    )

    def response_add(self, request, obj, post_url_continue=None):
        """Keep the same url on "Save and add one another"""
        res = super().response_add(request, obj, post_url_continue)
        if "_addanother" in request.POST:
            redirect_url = request.path + ('?extra=' if 'extra' in request.GET else '')
            return HttpResponseRedirect(redirect_url)
        else:
            return res

    def get_form(self, request, obj=None, change=False, **kwargs):
        """Return custom form on ?extra= URL"""
        if obj is None and 'extra' in request.GET:
            kwargs['form'] = CreateExtraTrainingForm
        else:
            kwargs['form'] = ChangeTrainingForm
        return super().get_form(request, obj, change, **kwargs)

    def get_inlines(self, request, obj):
        if obj is not None or 'extra' not in request.GET:
            return (
                ViewAttendanceInline,
                AddAttendanceInline,
            )
        return (
            AddAttendanceInline,
        )

    def get_changeform_initial_data(self, request):
        """Custom form default values"""
        if 'extra' in request.GET:
            return {
                "group": Group.objects.get(semester=get_ongoing_semester(), name=settings.EXTRA_EVENTS_GROUP_NAME),
                "start": timezone.now().replace(minute=0, second=0),
                "end": timezone.now().replace(minute=30, second=0),
            }
        return {}

    def get_fieldsets(self, request, obj=None):
        return (
            (None, {
                'fields': ('group', 'start', 'end')
            }),
            ('Add attended students with same hours', {
                'fields': ('attended_students', 'hours',)
            }),
            ('Upload a csv file with attendance records', {
                'fields': ('csv',)
            }),
        )

    @transaction.atomic
    def save_related(self, request, form, formsets, change):
        """
        There are three ways of creating/changing attendance records (from highest priority to lowest):
        1) Upload CSV file
        2) Use ModelMultipleChoiceField in ModelAdmin for training
        3) Change/add attendance records using inline
        """
        super().save_related(request, form, formsets, change)
        training = form.instance
        similar_student_hours = [
            (student.pk, form.cleaned_data['hours'])
            for student in form.cleaned_data['attended_students']
        ]
        csv_student_hours = [
            (student.pk, hours)
            for (student, hours) in form.cleaned_data['attendances']
        ]
        mark_hours(training, OrderedDict(similar_student_hours + csv_student_hours).items())
        return training
