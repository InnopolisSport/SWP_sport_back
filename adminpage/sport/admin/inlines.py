from django.contrib import admin
from django.http import HttpRequest

from sport import models


class ViewAttendanceInline(admin.TabularInline):
    model = models.Attendance
    extra = 0
    fields = ("training", "student", "hours")
    readonly_fields = ("training", "student")
    autocomplete_fields = ("training", "student")
    ordering = ("-training__start", "student__user__first_name", "student__user__last_name")

    def has_add_permission(self, request, obj):
        return False

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            "training__group__semester",
            "student__user",
            "training__training_class"
        )


class AddAttendanceInline(ViewAttendanceInline):
    extra = 1
    verbose_name_plural = "Add extra attendance record"
    readonly_fields = ()

    def has_view_or_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj):
        return True


class ScheduleInline(admin.TabularInline):
    model = models.Schedule
    extra = 0
    ordering = ("weekday", "start")

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("group__semester", "training_class")


class EnrollInline(admin.TabularInline):
    model = models.Enroll
    extra = 0
    autocomplete_fields = ("student",)
    ordering = ("student__user__first_name", "student__user__last_name")

    def has_change_permission(self, request, obj=None):
        return False

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("student__user", "group__semester")


class GroupInline(admin.TabularInline):
    model = models.Group
    extra = 0
    ordering = ("semester", "name")


class TrainingInline(admin.TabularInline):
    model = models.Training
    fields = ("start", "end", "training_class")
    autocomplete_fields = ("training_class",)
    extra = 0
    ordering = ("-start",)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("training_class", "group__semester")


class ViewTrainingInline(TrainingInline):
    exclude = ("group",)
    extra = 0

    def has_add_permission(
            self, request: HttpRequest, *args, **kwargs
    ) -> bool:
        return False
