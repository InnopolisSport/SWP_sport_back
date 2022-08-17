from admin_auto_filters.filters import AutocompleteFilter
from django.conf import settings
from django.contrib import admin
from django.db.models.expressions import RawSQL
from django.utils.html import format_html
from django.forms import ModelForm
from django.forms import CheckboxSelectMultiple

from api.crud import get_ongoing_semester
from sport.models import Group, MedicalGroup
from .inlines import EnrollInline, TrainingInline
from .utils import custom_titled_filter, has_free_places_filter, DefaultFilterMixIn, ScheduleInline
from .site import site


class TrainerTextFilter(AutocompleteFilter):
    title = "trainer"
    field_name = "trainers"


class GroupAdminForm(ModelForm):
    class Meta:
        model = Group
        fields = '__all__'  # will be overridden by ModelAdmin
        widgets = {
            'allowed_medical_groups': CheckboxSelectMultiple()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['allowed_medical_groups'].initial = [2,1,0]


@admin.register(Group, site=site)
class GroupAdmin(DefaultFilterMixIn):
    semester_filter = 'semester__id__exact'

    form = GroupAdminForm

    search_fields = (
        "name",
        "sport__name",
        "trainers__user__first_name",
        "trainers__user__last_name",
        "trainers__user__email",
    )

    autocomplete_fields = (
        "sport",
        # "trainer",
        'trainers',
    )

    list_filter = (
        ("semester", admin.RelatedOnlyFieldListFilter),
        has_free_places_filter(),
        ("is_club", custom_titled_filter("club status")),
        TrainerTextFilter,
        ("sport", admin.RelatedOnlyFieldListFilter),
    )

    list_display = (
        "__str__",
        "is_club",
        "teachers",  # check function below
        "free_places",
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
    )

    fields = (
        "name",
        "description",
        ("link_name", "link"),
        ("capacity", "free_places"),
        "is_club",
        "sport",
        "semester",
        "trainers",
        "allowed_medical_groups",
    )

    readonly_fields = (
        "free_places",
    )

    def teachers(self, obj):
        return format_html(";<br>".join([t.user.first_name + ' ' + t.user.last_name for t in obj.trainers.all()]))

    def free_places(self, obj):
        return obj.capacity - obj.enroll_count

    # Dirty hack, filter autocomplete groups in "add extra form"
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if 'extra' in request.META.get('HTTP_REFERER', []):
            return qs.filter(semester=get_ongoing_semester(), sport=None).order_by('name')
        return qs.annotate(enroll_count=RawSQL('select count(*) from enroll where group_id = "group".id', ()))

    class Media:
        pass
