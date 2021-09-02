from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin
from django.contrib.auth.models import Group as DjangoGroup
from sport.models import FAQElement, FAQCategory

from .site import site


@admin.register(FAQElement, site=site)
class FAQAdmin(admin.ModelAdmin):
    list_display = (
        'question',
        format_answer,
        'category',
    )

    list_filter = (
        "category",
    )

    def format_answer(self, obj):
        return obj.answer.html()


@admin.register(FAQCategory, site=site)
class FAQAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )
