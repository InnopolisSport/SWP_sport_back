from django.contrib import admin

from sport.models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_filter = (
        "is_ill",
    )

    list_display = (
        "__str__",
        "is_ill",
    )
