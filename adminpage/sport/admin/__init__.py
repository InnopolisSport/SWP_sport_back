from django.contrib import admin

import sport.models as models
from .enrollAdmin import EnrollAdmin
from .fabrics import admin_with_filters_fabric, semester_filter_fabric

admin.site.register(models.Admin)
admin.site.register(models.Attendance)
admin.site.register(models.Enroll, EnrollAdmin)
admin.site.register(models.Group, admin_with_filters_fabric(
    semester_filter_fabric("semester__id")
))
admin.site.register(models.Schedule, admin_with_filters_fabric(
    semester_filter_fabric("group__semester__id")
))
admin.site.register(models.Semester)
admin.site.register(models.Sport)
admin.site.register(models.Student)
admin.site.register(models.Trainer)
admin.site.register(models.Training, admin_with_filters_fabric(
    semester_filter_fabric("group__semester__id")
))
