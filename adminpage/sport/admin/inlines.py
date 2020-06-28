from django.contrib import admin
from django.http import HttpRequest

from sport import models


class AttendanceInline(admin.TabularInline):
    model = models.Attendance
    extra = 1
    autocomplete_fields = ("training", "student")
    ordering = ("training__start", "student__user__first_name", "student__user__last_name")

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            "training__group__semester",
            "student__user",
            "training__training_class"
        )


class ScheduleInline(admin.TabularInline):
    model = models.Schedule
    extra = 1
    ordering = ("weekday", "start")

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("group__semester", "training_class")


class EnrollInline(admin.TabularInline):
    model = models.Enroll
    extra = 1
    autocomplete_fields = ("student",)
    ordering = ("student__user__first_name", "student__user__last_name")

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("student__user", "group__semester")


class GroupInline(admin.TabularInline):
    model = models.Group
    extra = 0
    ordering = ("semester", "name")


class TrainingInline(admin.TabularInline):
    model = models.Training
    autocomplete_fields = ("schedule", "training_class",)
    extra = 1
    ordering = ("start",)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("training_class", "group__semester")


class ViewTrainingInline(TrainingInline):
    exclude = ("group",)
    extra = 0

    def has_add_permission(
            self, request: HttpRequest, *args, **kwargs
    ) -> bool:
        return False
