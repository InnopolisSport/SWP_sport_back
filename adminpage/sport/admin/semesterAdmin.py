from django.contrib import admin
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from openpyxl import Workbook
from openpyxl.writer.excel import save_virtual_workbook

from sport.models import Semester
from .site import site


def export_hours_as_xlsx(modeladmin, request, queryset):
    field_names = ["Name", "Surname", "Email", "Hours"]
    work_book = Workbook(write_only=True)

    for semester in queryset:
        # student_hours = Student.objects\
        #     .filter(attendance__training__group__semester=semester)\
        #     .annotate(hours=Coalesce(Sum("attendance__hours"), 0))
        student_hours = get_user_model().objects.raw(
            "select u.id "
            "     , u.first_name "
            "     , u.last_name "
            "     , u.email "
            "     , coalesce(sum(a.hours), 0) as hours "
            "from student s "
            "         join auth_user u on s.user_id = u.id "
            "         left join ( "
            "    select * "
            "    from attendance a "
            "             join training t on a.training_id = t.id "
            "             join \"group\" g on t.group_id = g.id "
            "    where g.semester_id = %s "
            ") as a on s.id = a.student_id "
            "where s.user_id = u.id "
            "group by s.id, u.id "
            "order by u.last_name, u.first_name; ", [semester.pk])
        work_sheet = work_book.create_sheet(title=semester.name)
        work_sheet.append(field_names)
        for student in student_hours:
            work_sheet.append([student.first_name, student.last_name, student.email, student.hours])

    response = HttpResponse(save_virtual_workbook(work_book),
                            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename=SportHours_{"_".join(map(str, queryset.all()))}.xlsx'

    return response


export_hours_as_xlsx.short_description = "Export hours for selected semesters"


@admin.register(Semester, site=site)
class SemesterAdmin(admin.ModelAdmin):
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
        "choice_deadline",
    )

    actions = (
        export_hours_as_xlsx,
    )
