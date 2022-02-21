from django.contrib import admin
from sport.admin import StudentAdmin, site
from sport.models import Student


def create_modeladmin(model, name = None):
    class  Meta:
        proxy = True
        app_label = model._meta.app_label
        verbose_name = "Student (normal)"
        verbose_name_plural = "Students (normal)"

    attrs = {'__module__': '', 'Meta': Meta}

    newmodel = type(name, (model,), attrs)

    return newmodel


@admin.register(create_modeladmin(Student, "studentNormal"), site=site)
class NormalStudentAdmin(StudentAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request).filter(student_status=0)

