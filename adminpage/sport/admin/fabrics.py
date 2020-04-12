from typing import List, Tuple, Any, Optional

from django.contrib import admin
from django.db.models import QuerySet

import sport.models as models


def semester_filter_fabric(filtering_field: str):
    class SemesterFilter(admin.SimpleListFilter):
        title = "semester"
        parameter_name = "semester"
        default_value = None  # TODO: set the current semester as default

        def lookups(self, request, model_admin) -> List[Tuple[Any, str]]:
            qs = models.Semester.objects.all()
            return sorted(
                ((semester.id, semester.name) for semester in qs),
                # Sort by semester name: by year, then by letter
                key=lambda x: (int(x[1][1:]), x[1][0]),
                reverse=True
            )

        def queryset(self, request: Any, queryset: QuerySet) -> Optional[QuerySet]:
            if self.value():
                return queryset.filter(**{
                    filtering_field: self.value()
                })
            else:
                return queryset

    return SemesterFilter


def admin_with_filters_fabric(*args):
    class FilteredAdmin(admin.ModelAdmin):
        list_filter = args

    return FilteredAdmin
