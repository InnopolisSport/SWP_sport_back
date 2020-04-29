from django.http import HttpResponse
from openpyxl import Workbook
from openpyxl.writer.excel import save_virtual_workbook

from sport.models import Semester


class EnrollExportXlsxMixin:
    def export_as_csv(self, request, queryset):
        field_names = ["Sport", "Fullname", "Email"]
        semester_id = request.GET.get("semester")
        work_book = Workbook(write_only=True)
        if semester_id is None:
            semester_name = "all"
        else:
            semester_name = Semester.objects.get(pk=semester_id).name

        work_sheet = work_book.create_sheet(title=semester_name)
        work_sheet.append(field_names)

        for obj in queryset:
            if not obj.is_primary:
                continue
            group = obj.group
            sport = group.sport
            sport_name = "Personal Trainer" if sport.special and not group.is_club else sport.name

            student_fullname = str(obj.student)
            student_email = obj.student.email
            work_sheet.append([sport_name, student_fullname, student_email])

        response = HttpResponse(save_virtual_workbook(work_book),
                                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename=SportEnrollment_{semester_name}.xlsx'

        return response

    export_as_csv.short_description = "Export primary sport groups"
