from django.contrib import admin
from django.db.models import Q

from sport.admin.utils import InputFilter
from sport.models import Attendance


class StudentFilter(InputFilter):
    parameter_name = 'student'
    title = 'student'

    def queryset(self, request, queryset):
        if self.value() is not None:
            search = self.value().split()
            if len(search) == 0:
                return queryset
            if len(search) == 1:
                return queryset.filter(
                    Q(student__first_name=search[0]) |
                    Q(student__last_name=search[0]) |
                    Q(student__email=search[0])
                )
            return queryset.filter(
                Q(student__first_name__in=search) &
                Q(student__last_name__in=search) |
                Q(student__email=search[0])
            )


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    # TODO: test performance
    # https://docs.djangoproject.com/en/3.0/ref/contrib/admin/#django.contrib.admin.ModelAdmin.autocomplete_fields
    autocomplete_fields = (
        "training",
        "student",
    )

    list_display = (
        "student",
        "training",
        "hours",
    )

    list_filter = (
        "training__group__semester",
        ("training__group", admin.RelatedOnlyFieldListFilter),
        StudentFilter,
        "training__start",
    )

    class Media:
        js = (
            "sport/js/list_filter_collapse.js",
        )
