from admin_auto_filters.filters import AutocompleteFilter
from django.conf import settings
from django.contrib import admin

from api.crud import get_ongoing_semester
from sport.models import Group
from .inlines import ScheduleInline, EnrollInline, TrainingInline
from .utils import custom_titled_filter
from .site import site


class TrainerTextFilter(AutocompleteFilter):
    title = "trainer"
    field_name = "trainer"


@admin.register(Group, site=site)
class GroupAdmin(admin.ModelAdmin):
    search_fields = (
        "name",
    )

    autocomplete_fields = (
        "sport",
        "trainer",
    )

    list_filter = (
        ("semester", admin.RelatedOnlyFieldListFilter),
        ("is_club", custom_titled_filter("club status")),
        TrainerTextFilter,
        "minimum_medical_group",
        ("sport", admin.RelatedOnlyFieldListFilter),
    )

    list_display = (
        "__str__",
        "sport",
        "is_club",
        "trainer",
        "minimum_medical_group",
    )

    inlines = (
        ScheduleInline,
        TrainingInline,
        EnrollInline,
    )

    list_select_related = (
        "semester",
        "sport",
        "trainer__user",
        "minimum_medical_group",
    )

    # Dirty hack, filter autocomplete groups in "add extra form"
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if 'extra' in request.META.get('HTTP_REFERER', []):
            return qs.filter(semester=get_ongoing_semester(), sport__name=settings.OTHER_SPORT_NAME).order_by('name')
        return qs

    class Media:
        pass
