from django.contrib import admin

from sport.models import Student
from .inlines import AttendanceInline


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    search_fields = (
        "first_name",
        "last_name",
        "email",
    )

    list_filter = (
        "is_ill",
    )

    list_display = (
        "__str__",
        "is_ill",
    )

    inlines = (
        AttendanceInline,
    )
