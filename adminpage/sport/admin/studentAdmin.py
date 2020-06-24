from django.contrib import admin
from django.contrib.auth import get_user_model
from import_export import resources, widgets, fields
from import_export.admin import ImportMixin

from sport.models import Student, enums
from sport.signals import get_or_create_student_group
from .inlines import AttendanceInline
from .utils import user__email
from .site import site


class MedicalGroupWidget(widgets.NumberWidget):
    def render(self, value, obj=None):
        return enums.MedicalGroups.labels[int(value) + 2]


class StudentResource(resources.ModelResource):
    medical_group = fields.Field(column_name="medical_group", attribute="medical_group", widget=MedicalGroupWidget())

    def before_import(self, dataset, dry_run, *args, **kwargs):
        user_ids = []
        student_group = get_or_create_student_group()
        user_model = get_user_model()
        for data in dataset.dict:
            email = data["email"]

            user, _ = user_model.objects.get_or_create(
                email=email,
                defaults={
                    "first_name": data["first_name"],
                    "last_name": data["last_name"],
                    "username": data["email"],
                }
            )

            user.groups.add(student_group)
            user_ids.append(user.pk)
        dataset.insert_col(0, user_ids, "user")
        return super(StudentResource, self).before_import(dataset, dry_run, *args, **kwargs)

    class Meta:
        model = Student
        fields = (
            "user",
            "user__email",
            "user__first_name",
            "user__last_name",
        )
        export_order = (
            "user",
            "user__email",
            "user__first_name",
            "user__last_name",
            "medical_group",
        )
        import_id_fields = ("user",)


@admin.register(Student, site=site)
class StudentAdmin(ImportMixin, admin.ModelAdmin):
    resource_class = StudentResource
    
    search_fields = (
        "user__first_name",
        "user__last_name",
        "user__email",
    )

    list_filter = (
        "is_ill",
        "medical_group",
    )

    list_display = (
        "__str__",
        user__email,
        "is_ill",
        "medical_group",
    )

    ordering = (
        "user__first_name",
        "user__last_name"
    )

    inlines = (
        AttendanceInline,
    )
