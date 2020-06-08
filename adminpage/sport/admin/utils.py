from typing import List, Dict

from django.contrib import admin

from sport.models import Semester


def custom_titled_filter(title, filter_class=admin.RelatedFieldListFilter):
    class Wrapper(filter_class):
        def __new__(cls, *args, **kwargs):
            instance = filter_class.create(*args, **kwargs)
            instance.title = title
            return instance

    return Wrapper


def cache_filter(cls, clear_list: List[str]):
    """
    Overrides filter methods, so that chosen filter value will be available to other filters
    @param cls: used filter class
    @param clear_list: list of query fields that should be cleared, when some choice within this filter is selected.
    Useful for clearing dependent sub filters (clear semester choice, when study year is selected).
    """

    def add_value_to_cache(request, param, value):
        try:
            request.cache_filter[param] = value
        except:
            request.cache_filter = {param: value}

    class CacheAwareFilter(cls):
        def lookups(self, request, model_admin):
            add_value_to_cache(request, self.parameter_name, self.value())
            return super().lookups(request, model_admin)

        def field_choices(self, field, request, model_admin):
            add_value_to_cache(request, self.field_path, self.lookup_val)
            return super().field_choices(field, request, model_admin)

        def choices(self, changelist):
            # save previous version of get_query_string that is used in super().choices(changelist)
            f = changelist.get_query_string

            def get_query_string(new_params=None, remove=None):
                # call prior version with additional 'remove' fields
                return f(new_params=new_params, remove=clear_list if remove is None else (clear_list + remove))

            # override get_query_string
            changelist.get_query_string = get_query_string
            yield from super().choices(changelist)
            # revert to original get_query_string, since it can be used further
            changelist.get_query_string = f

    return CacheAwareFilter


def cache_dependent_filter(translation: Dict[str, str]):
    """
    Creates foreign key list filter, that can use cached values from other filters
    @param translation: rules for translating cached keys, if 'key' is cached,
    translation['key'] will be used as the actual filter parameter
    """

    class CacheRelatedFieldListFilter(admin.RelatedFieldListFilter):
        def field_choices(self, field, request, model_admin):
            self.no_output = any(map(lambda x: request.cache_filter[x] is None, translation))
            if self.no_output:
                return []
            additional_filter = {translation[k]: request.cache_filter[k] for k in translation}
            ordering = self.field_admin_ordering(field, request, model_admin)
            return field.get_choices(include_blank=False, ordering=ordering,
                                     limit_choices_to=additional_filter)

        def has_output(self):
            return not self.no_output

    return CacheRelatedFieldListFilter


def cache_alternative_filter(cls, cache_keys: List[str]):
    """
    Creates foreign key list filter, that will be used when one of the cache value is empty
    @param cache_keys: used cached keys, if an associated value for some given 'key' is None,
    filter will be rendered
    """

    class CacheRelatedFieldListFilter(cls):
        def __init__(self, field, request, *args, **kwargs):
            self.no_output = any(map(lambda x: request.cache_filter[x] is None, cache_keys))
            super().__init__(field, request, *args, **kwargs)

        def has_output(self):
            return self.no_output

    return CacheRelatedFieldListFilter


def year_filter(year_field: str):
    class YearFilter(admin.SimpleListFilter):
        title = "study year"
        parameter_name = year_field

        def lookups(self, request, model_admin):
            years = list(Semester.objects.all().values("start__year").distinct())
            return list(map(lambda x: (x["start__year"], x["start__year"]), years))

        def queryset(self, request, queryset):
            if self.value() is not None:
                return queryset.filter(**{year_field: self.value()})

    return YearFilter
