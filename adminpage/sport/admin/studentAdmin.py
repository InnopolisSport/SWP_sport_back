from django.contrib import admin
from django.contrib.auth import get_user_model
from import_export.widgets import ForeignKeyWidget

from sport.models import Student
from .inlines import AttendanceInline
from .utils import user__email
from import_export import resources, fields
from import_export.admin import ImportMixin

from sport.signals import get_or_create_student_group


class StudentResource(resources.ModelResource):

    def before_import(self, dataset, dry_run, *args, **kwargs):
        user_ids = []
        for data in dataset.dict:
            email = data["email"]

            user, _ = get_user_model().objects.get_or_create(
                email=email,
                defaults={
                    "first_name": data["first_name"],
                    "last_name": data["last_name"],
                    "username": data["email"],
                }
            )

            user.groups.add(get_or_create_student_group())
            user_ids.append(user.pk)
        dataset.insert_col(0, user_ids, "user")
        return super(StudentResource, self).before_import(dataset, dry_run, *args, **kwargs)

    class Meta:
        model = Student
        fields = (
            "user",
            "email",
            "first_name",
            "last_name",
            "is_ill",
            "medical_group",
        )
        import_id_fields = ("user",)


@admin.register(Student)
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
