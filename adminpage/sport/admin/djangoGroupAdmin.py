from django.contrib import admin
from django.contrib.auth.models import Group as DjangoGroup

admin.site.unregister(DjangoGroup)


@admin.register(DjangoGroup)
class DjangoGroupAdmin(admin.ModelAdmin):
    list_display = (
        'verbose_name',
        'name',
    )
