from django.contrib import admin
from django.contrib.auth import get_user_model
from django.db.models import ForeignKey, IntegerField, F, Sum
from django.db.models.expressions import Value, Case, When, Subquery, OuterRef, ExpressionWrapper
from django.db.models.functions import Coalesce, Least
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from import_export import resources, widgets, fields
from import_export.admin import ImportExportActionModelAdmin
from import_export.results import RowResult

from api.crud import get_ongoing_semester, get_negative_hours
from sport.models import Student, MedicalGroup, StudentStatus, Semester, Sport, Attendance, Debt
from sport.signals import get_or_create_student_group
from .inlines import ViewAttendanceInline, AddAttendanceInline, ViewMedicalGroupHistoryInline
from .site import site
from .utils import SumSubquery, user__role


class MedicalGroupWidget(widgets.ForeignKeyWidget):
    def render(self, value: MedicalGroup, obj=None):
        return str(value)


class StudentStatusWidget(widgets.ForeignKeyWidget):
    def render(self, value: StudentStatus, obj=None):
        return str(value)


class HoursFilter(admin.SimpleListFilter):
    title = 'debt'
    parameter_name = 'debt'

    def lookups(self, request, model_admin):
        return (
            ('Yes', 'Yes'),
            ('No', 'No'),
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value == 'Yes':
            return queryset.filter(complex_hours__lt=0)
        elif value == 'No':
            return queryset.exclude(complex_hours__lt=0)
        return queryset


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

    sport = fields.Field(
        column_name="sport",
        attribute="sport",
        widget=StudentStatusWidget(Sport, "pk"),
    )

    complex_hours = fields.Field(attribute='complex_hours', readonly=True)

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
            "is_online",
        )
        export_order = (
            "user",
            "user__email",
            "user__first_name",
            "user__last_name",
            "enrollment_year",
            "course",
            "medical_group",
            "student_status",
            "is_online",
            'sport',
            'complex_hours',
            "telegram",
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
class StudentAdmin(ImportExportActionModelAdmin):
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
        "course",
        "enrollment_year",
        "is_online",
        "medical_group",
        'student_status',
        'sport',
        HoursFilter
    )

    list_display = (
        "__str__",
        user__role,
        "is_online",
        "course",
        "medical_group",
        "sport",
        "complex_hours",
        "student_status",
        "write_to_telegram",
    )

    readonly_fields = (
        "write_to_telegram",
    )

    def write_to_telegram(self, obj):
        return None if obj.telegram is None else \
            format_html(
                '<a target="_blank" href="https://t.me/{}">{}</a>',
                obj.telegram[1:],
                obj.telegram
            )

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

        qs = qs.annotate(_debt=Coalesce(
            SumSubquery(Debt.objects.filter(semester_id=get_ongoing_semester().pk,
                                            student_id=OuterRef("pk")), 'debt'),
            0
        ))
        qs = qs.annotate(_ongoing_semester_hours=Coalesce(
            SumSubquery(Attendance.objects.filter(training__group__semester_id=get_ongoing_semester().pk, student_id=OuterRef("pk")), 'hours'),
            0
        ))
        qs = qs.annotate(complex_hours=ExpressionWrapper(
            F('_ongoing_semester_hours') - F('_debt'), output_field=IntegerField()
        ))

        return qs


    list_select_related = (
        "user",
        "medical_group",
    )
