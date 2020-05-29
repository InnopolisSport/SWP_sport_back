from django.contrib import admin

from sport.models import TrainingClass


@admin.register(TrainingClass)
class TrainingClassAdmin(admin.ModelAdmin):
    pass
