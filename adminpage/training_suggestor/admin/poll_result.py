from django.contrib import admin

from training_suggestor.admin.site import site
from training_suggestor.models import PollResult, PollAnswer


class PollAnswerInline(admin.TabularInline):
    model = PollAnswer

    # TODO:
    # def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
    #     field = super().formfield_for_foreignkey(db_field, request, **kwargs)
    #     print(request)
    #     if db_field.name == 'question':
    #         if hasattr(request, '_obj_') and request._obj_ is not None:
    #             field.queryset = field.queryset.filter(poll=request._obj_.poll)
    #         else:
    #             field.queryset = field.queryset.none()
    #
    #     return field


@admin.register(PollResult, site=site)
class PollResultAdmin(admin.ModelAdmin):
    list_display = ('poll', 'user', 'created')
    readonly_fields = ('created',)
    inlines = (PollAnswerInline,)
