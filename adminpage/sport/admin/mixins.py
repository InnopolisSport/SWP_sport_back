from django.db.models import QuerySet
from django.http import HttpResponse
from openpyxl import Workbook
from openpyxl.writer.excel import save_virtual_workbook

from sport.models import Semester


class EnrollExportXlsxMixin:
    def export_as_csv(self, request, queryset: QuerySet):
        field_names = ["Group", "Fullname", "Email",
                       "Monday", "Tuesday", "Wednesday",
                       "Thursday", "Friday", "Saturday",
                       "Sunday", ]
        semester_id = request.GET.get("semester")
        work_book = Workbook(write_only=True)
        if semester_id is None:
            semester_name = "all"
        else:
            semester_name = Semester.objects.get(pk=semester_id).name

        work_sheet = work_book.create_sheet(title=semester_name)
        work_sheet.append(field_names)

        for enrollment in queryset.order_by("group").select_related("group").prefetch_related("group__schedule"):
            if not enrollment.is_primary:
                continue
            group = enrollment.group

            schedule = [""] * 7
            if group.schedule.exists():
                for scheduled_training in group.schedule.all():
                    schedule[scheduled_training.weekday] += f"{scheduled_training.start}-{scheduled_training.end}\n\n"

            student_fullname = str(enrollment.student)
            student_email = enrollment.student.user.email
            data = [group.name, student_fullname, student_email, *schedule]

            work_sheet.append(data)

        response = HttpResponse(save_virtual_workbook(work_book),
                                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename=SportEnrollment_{semester_name}.xlsx'

        return response

    export_as_csv.short_description = "Export primary sport groups"
