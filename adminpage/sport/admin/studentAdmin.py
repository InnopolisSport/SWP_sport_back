from django.contrib import admin

from sport.models import Student
from .inlines import AttendanceInline
from .utils import user__email
from .site import site


@admin.register(Student, site=site)
class StudentAdmin(admin.ModelAdmin):
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
