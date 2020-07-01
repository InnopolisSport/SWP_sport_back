from datetime import date

from admin_auto_filters.filters import AutocompleteFilter
from django.contrib import admin
from django.db.models import Sum, Subquery, OuterRef
from django.db.models.functions import Coalesce
from django.http import HttpResponse
from import_export.admin import ExportMixin
from openpyxl import Workbook
from openpyxl.writer.excel import save_virtual_workbook
from rangefilter.filter import DateRangeFilter

from sport.admin.utils import cache_filter, cache_dependent_filter, custom_order_filter
from sport.models import Attendance, Student, Semester
from .site import site


class StudentTextFilter(AutocompleteFilter):
    title = "student"
    field_name = "student"


def export_attendance_as_xlsx(modeladmin, request, queryset):
    semester_id = request.GET.get("training__group__semester__id__exact", None)
    date_start_str = request.GET.get("training__start__range__gte", None)
    date_end_str = request.GET.get("training__start__range__lte", None)

    export_period = ""
    if semester_id is not None:
        semester = Semester.objects.get(id=semester_id)
        export_period = f"Semester {semester.name} ({semester.start} - {semester.end})"
    elif date_start_str is not None:
        export_period = f"{date_start_str} - {date_end_str if date_end_str else date.today()}"
    else:
        modeladmin.message_user(request, "Please filter by semester or specify training start range")

    collected_hours = queryset.values("student_id").annotate(
        collected_hours=Sum('hours')
    ).filter(student_id=OuterRef("user_id")).values('collected_hours')

    student_data = Student.objects.annotate(
        collected_hours=Coalesce(Subquery(collected_hours), 0)
    ).select_related("user")

    wb = Workbook(write_only=True)
    ws = wb.create_sheet(export_period)
    ws.append(["Exported attendance for", export_period])
    ws.append(["email", "hours"])
    for student in student_data:
        ws.append([student.user.email, student.collected_hours])
    response = HttpResponse(save_virtual_workbook(wb),
                            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename=SportHours_{export_period}.xlsx'

    return response


@admin.register(Attendance, site=site)
class AttendanceAdmin(admin.ModelAdmin):
    # TODO: test performance
    # https://docs.djangoproject.com/en/3.0/ref/contrib/admin/#django.contrib.admin.ModelAdmin.autocomplete_fields
    autocomplete_fields = (
        "training",
        "student",
    )

    list_display = (
        "student",
        "training",
        "hours",
    )

    ordering = (
        "-training__start",
    )

    actions = (
        export_attendance_as_xlsx,
    )

    list_filter = (
        StudentTextFilter,
        ("training__start", DateRangeFilter),
        # semester filter, resets group sub filter
        (
            "training__group__semester",
            cache_filter(custom_order_filter(("-start",)), ["training__group__id"])
        ),
        # group filter, depends on chosen semester
        (
            "training__group",
            cache_dependent_filter({"training__group__semester": "semester__pk"}, ("name",),
                                   select_related=["semester"])
        ),
    )

    list_select_related = (
        "student__user",
        "training__group",
        "training__group__semester",
        "training__training_class",
    )

    class Media:
        pass
