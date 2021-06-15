from typing import Optional

from django.contrib import admin
from django.db.models import Model
from django.http import HttpRequest

from sport.models import StudentStatus
from .site import site


@admin.register(StudentStatus, site=site)
class StudentStatusAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    fields = ("name", "description")

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request: HttpRequest, obj: Optional[Model] = ...) -> bool:
        return False
