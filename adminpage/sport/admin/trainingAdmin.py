import io
from collections import OrderedDict

from django.urls import path
from openpyxl import load_workbook

from django.conf import settings
from django.contrib import admin
from django import forms
from django.contrib.admin.widgets import AutocompleteSelectMultiple, AdminDateWidget
from django.db import transaction
from django.utils import timezone

import datetime
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
    xlsx = forms.FileField(required=False, widget=forms.FileInput(attrs={'accept': '.xlsx'}))

    def clean(self):
        cleaned_data = super().clean()
        attendances = []
        cleaned_data['attendances'] = attendances
        file = cleaned_data.get("xlsx", None)
        if file is None:
            return cleaned_data
        data = file.read()
        emails = []
        hours = {}
        ws = load_workbook(filename=io.BytesIO(data), read_only=True).active
        for i, row in enumerate(ws):
            if i == 0:
                if len(row) != 2:
                    raise forms.ValidationError(f"Expected 2 columns header, got {len(row)} columns")
                header = [row[0].value, row[1].value]
                if header != ["email", "hours"]:
                    raise forms.ValidationError(f"Missing header ['email', 'hours'], got: {header}")
                continue

            if len(row) != 2:
                raise forms.ValidationError(f"Expected 2 columns in each row, got {len(row)} columns in row {i + 1}")
            email, student_hours = row[0].value, row[1].value
            emails.append(email)
            try:
                hours[email] = round(float(student_hours), 2)
                assert 0 <= hours[email] < 1000  # TODO: hardcoded constant
            except (AssertionError, ValueError, TypeError):
                raise forms.ValidationError(
                    f"Got invalid hours value \"{student_hours}\" for email {email}, expected value in range [0,999.99]"
                )
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
    event_name = forms.CharField(label='Event name', max_length=100, required=False)
    start_day = forms.DateField(
        label='Event start day',
        initial=timezone.now().date(),
        widget=AdminDateWidget(attrs={'size': 16})
    )
    end_day = forms.DateField(
        label='Event end day',
        required=False,
        widget=AdminDateWidget(attrs={'size': 16})
    )

    class Meta:
        model = Training
        fields = ('group', 'event_name', 'start_day', 'end_day')

    def save(self, commit=True):
        self.instance.start = datetime.datetime.combine(
            self.cleaned_data['start_day'],
            datetime.time(0, 0, 0),
            tzinfo=timezone.localtime().tzinfo
        )
        self.instance.end = datetime.datetime.combine(
            self.cleaned_data['start_day' if self.cleaned_data['end_day'] is None else 'end_day'],
            datetime.time(23, 59, 59),
            tzinfo=timezone.localtime().tzinfo
        )
        if len(self.cleaned_data['event_name']) > 0:
            self.instance.custom_name = self.cleaned_data['event_name']
        return super().save(commit)


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
        "custom_name",
        "start",
        "end",
        "training_class",
    )

    readonly_fields = (
        "custom_name",
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

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('add-extra/', self.extra_add, name='sport_training_add_extra'),
        ]
        return custom_urls + urls

    def extra_add(self, request):
        return self.changeform_view(request, None, '', None)

    def get_form(self, request, obj=None, change=False, **kwargs):
        kwargs['form'] = CreateExtraTrainingForm if 'add-extra' in request.path else ChangeTrainingForm
        return super().get_form(request, obj, change, **kwargs)

    def get_inlines(self, request, obj):
        if obj is not None or 'add-extra' not in request.path:
            return (
                ViewAttendanceInline,
                AddAttendanceInline,
            )
        return (
            AddAttendanceInline,
        )

    def get_changeform_initial_data(self, request):
        """Custom form default values"""
        if 'add-extra' in request.path:
            return {
                'group': Group.objects.get(semester=get_ongoing_semester(), name=settings.EXTRA_EVENTS_GROUP_NAME)
            }
        return {}

    def get_fieldsets(self, request, obj=None):
        return (
            (None, {
                'fields': ('group', 'event_name', ('start_day', 'end_day'))
                if 'add-extra' in request.path
                else ('group' if obj is None or obj.custom_name is None else ('group', 'custom_name'), 'start', 'end')
            }),
            ('Add attended students with same hours', {
                'fields': ('attended_students', 'hours',)
            }),
            ('Upload a xlsx file with attendance records', {
                'fields': ('xlsx',)
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
        xlsx_student_hours = [
            (student.pk, hours)
            for (student, hours) in form.cleaned_data['attendances']
        ]
        mark_hours(training, OrderedDict(similar_student_hours + xlsx_student_hours).items())
        return training
