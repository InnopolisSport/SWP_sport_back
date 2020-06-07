from django.contrib import admin
from django.db import models


def custom_titled_filter(title, filter_class=admin.RelatedFieldListFilter):
    class Wrapper(filter_class):
        def __new__(cls, *args, **kwargs):
            instance = filter_class.create(*args, **kwargs)
            instance.title = title
            return instance

    return Wrapper


def year_filter(model: models.Model, year_field: str):
    class YearFilter(admin.SimpleListFilter):
        title = 'study year'
        parameter_name = year_field

        def lookups(self, request, model_admin):
            years = list(model.objects.all().values(year_field).distinct())
            return list(map(lambda x: (x[year_field], x[year_field]), years))

        def queryset(self, request, queryset):
            if self.value() is not None:
                return queryset.filter(start__year=self.value())
    return YearFilter
