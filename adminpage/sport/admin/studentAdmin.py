from django.contrib import admin
from django.contrib.auth import get_user_model
from django.db.models import ForeignKey, IntegerField, Count, DecimalField
from django.db.models.expressions import RawSQL, Value, Case, When, Subquery, OuterRef, ExpressionWrapper
from django.db.models.functions import Coalesce, Least
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from import_export import resources, widgets, fields
from import_export.admin import ImportMixin
from import_export.results import RowResult

from django.db.models import F, Q, Sum

from api.crud import get_brief_hours, get_ongoing_semester, get_detailed_hours, get_negative_hours
from sport.models import Student, MedicalGroup, StudentStatus, Semester
from sport.signals import get_or_create_student_group
from .inlines import ViewAttendanceInline, AddAttendanceInline, ViewMedicalGroupHistoryInline
from .site import site
from .utils import user__email, user__role


class MedicalGroupWidget(widgets.ForeignKeyWidget):
    def render(self, value: MedicalGroup, obj=None):
        return str(value)


class StudentStatusWidget(widgets.ForeignKeyWidget):
    def render(self, value: StudentStatus, obj=None):
        return str(value)


class StudentResource(resources.ModelResource):
    medical_group = fields.Field(
        column_name="medical_group",
        attribute="medical_group",
        widget=MedicalGroupWidget(MedicalGroup, "pk"),
    )

    student_status = fields.Field(
        column_name="student_status",
        attribute="student_status",
        widget=StudentStatusWidget(StudentStatus, "pk"),
    )

    def get_or_init_instance(self, instance_loader, row):
        student_group = get_or_create_student_group()
        user_model = get_user_model()
        user, _ = user_model.objects.get_or_create(
            email=row["email"],
            defaults={
                "first_name": row.get("first_name"),
                "last_name": row.get("last_name"),
            },
        )

        student_model_fields = [
            f.name
            for f in Student._meta.fields
            if not isinstance(f, ForeignKey)
        ]

        student_import_fields = row.keys() & student_model_fields

        student, student_created = Student.objects.get_or_create(
            user=user,
            defaults=dict([
                (key, row[key])
                for key in student_import_fields
            ])
        )
        if student_created:
            user.groups.add(student_group)

        return student, student_created

    class Meta:
        model = Student
        fields = (
            "user",
            "user__email",
            "user__first_name",
            "user__last_name",
            "enrollment_year",
            "course",
            "telegram",
        )
        export_order = (
            "user",
            "user__email",
            "user__first_name",
            "user__last_name",
            "medical_group",
            "enrollment_year",
            "course",
            "telegram",
            "student_status",
        )
        import_id_fields = ("user",)
        skip_unchanged = False
        report_skipped = True
        raise_errors = False

    def import_row(self, row, instance_loader, **kwargs):
        # overriding import_row to ignore errors and skip rows that fail to import
        # without failing the entire import
        import_result = super().import_row(row, instance_loader, **kwargs)
        if import_result.import_type == RowResult.IMPORT_TYPE_ERROR:
            # Copy the values to display in the preview report
            import_result.diff = [
                None,
                row.get('email'),
                row.get('first_name'),
                row.get('last_name'),
                row.get('medical_group'),
                row.get('enrollment_year'),
                row.get('course'),
                row.get('telegram'),
            ]
            # Add a column with the error message
            import_result.diff.append(mark_safe(
                f'''Errors:<ul>{''.join([f'<li>{err.error}</li>' for err in import_result.errors])}</ul>'''
            ))
            # clear errors and mark the record to skip
            import_result.errors = []
            import_result.import_type = RowResult.IMPORT_TYPE_SKIP

        return import_result


@admin.register(Student, site=site)
class StudentAdmin(ImportMixin, admin.ModelAdmin):
    resource_class = StudentResource

    def get_fields(self, request, obj=None):
        if obj is None:
            return (
                "user",
                "medical_group",
                "enrollment_year",
                "course",
                "student_status",
                "telegram",
            )
        return (
            "user",
            "is_ill",
            "is_online",
            "medical_group",
            "enrollment_year",
            "course",
            "sport",
            "student_status",
            "hours",
            "telegram" if obj.telegram is None or len(obj.telegram) == 0 else ("telegram", "write_to_telegram"),
        )

    autocomplete_fields = (
        "user",
    )

    search_fields = (
        "user__first_name",
        "user__last_name",
        "user__email",
        "telegram",
    )

    list_filter = (
        "is_online",
        "enrollment_year",
        "course",
        "medical_group",
        'student_status',
    )

    list_display = (
        "__str__",
        user__role,
        "is_online",
        "course",
        "medical_group",
        "sport",
        "hours",
        "complex_hours",
        "student_status",
        "write_to_telegram",
    )

    readonly_fields = (
        "hours",
        "write_to_telegram",
    )

    def write_to_telegram(self, obj):
        return None if obj.telegram is None else \
            format_html(
                '<a target="_blank" href="https://t.me/{}">{}</a>',
                obj.telegram[1:],
                obj.telegram
            )

    def hours(self, obj):
        return get_negative_hours(obj.user_id)

    def complex_hours(self, obj: Student):
        return obj.complex_hours

    complex_hours.admin_order_field = 'complex_hours'

    ordering = (
        "user__first_name",
        "user__last_name"
    )

    inlines = (
        ViewMedicalGroupHistoryInline,
        ViewAttendanceInline,
        AddAttendanceInline,
    )

    # https://stackoverflow.com/a/66730984
    def change_view(self, request, object_id, form_url='', extra_context=None):
        try:
            obj = self.model.objects.get(pk=object_id)
        except self.model.DoesNotExist:
            pass
        else:
            if obj.medical_group.name == 'Medical checkup not passed':
                self.inlines = (ViewAttendanceInline,)
        return super().change_view(request, object_id, form_url, extra_context)

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Get all hours for ongoing semester
        qs = qs.annotate(ongoing_semester_hours=Coalesce(Sum("attendance__hours",
                                                filter=Q(attendance__student=F("pk")) &
                                                       Q(attendance__training__group__semester=get_ongoing_semester())), 0))

        # To get previous semesters for current student exclude: (see comments below)
        previous_semesters_for_current_student = (
            Semester.objects
                .filter(end__lt=get_ongoing_semester().start)  # ongoing semester;
                .exclude(academic_leave_students=OuterRef("pk"))  # academic-leave semesters for current student;
                .exclude(end__year__lt=OuterRef("enrollment_year"))  # semesters, which current student wasn't enrolled.
        )

        # Get debt from previous semesters
        qs = qs.annotate(debt=Coalesce(Subquery(
            # TODO: Analyse answer https://stackoverflow.com/a/43771738 and complexity
            previous_semesters_for_current_student
                .values('hours').annotate(sum_hours=Sum('hours')).values('sum_hours')
        ), 0))

        # Get all hours for previous semesters
        qs = qs.annotate(last_semesters_hours=Coalesce(Sum("attendance__hours",
                                                        filter=Q(attendance__student=F("pk")) &
                                                               Q(attendance__training__group__semester__in=Subquery(previous_semesters_for_current_student.values('id')))), 0))

        qs = qs.annotate(complex_hours=ExpressionWrapper(F('ongoing_semester_hours') + Least(F('last_semesters_hours') - F('debt'), Value(0)), output_field=IntegerField()))
        print(qs.query)
        print(qs.values())
        return qs


    list_select_related = (
        "user",
        "medical_group",
    )
