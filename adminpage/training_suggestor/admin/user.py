from django.contrib import admin

from training_suggestor.admin import site
from training_suggestor.models import User


@admin.register(User, site=site)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'student')
