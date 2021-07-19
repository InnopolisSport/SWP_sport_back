import operator
from typing import List, Dict, Tuple

from django.contrib import admin
from django.db.models.expressions import F
from django.utils.translation import gettext_lazy as _


def user__email(obj):
    return obj.user.email


user__email.short_description = 'user email'


def user__role(obj):
    return obj.user.role


user__role.short_description = 'group'


def custom_order_filter(ordering: Tuple, cls=admin.RelatedFieldListFilter):
    class Wrapper(cls):
        def field_admin_ordering(self, field, request, model_admin):
            return ordering

    return Wrapper


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

        def has_output(self):
            return True

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


def cache_dependent_filter(translation: Dict[str, str], order=None, select_related: List[str] = None):
    """
    Creates foreign key list filter, that can use cached values from other filters
    @param translation: rules for translating cached keys, if 'key' is cached,
    @param order: desired filter list ordering
    @param select_related: related fields for faster lookup in one sql query
    translation['key'] will be used as the actual filter parameter
    """

    class CacheRelatedFieldListFilter(admin.RelatedFieldListFilter):
        def field_choices(self, field, request, model_admin):
            self.no_output = any(map(lambda x: request.cache_filter[x] is None, translation))
            if self.no_output:
                return []
            additional_filter = {translation[k]: request.cache_filter[k] for k in translation}
            ordering = order or self.field_admin_ordering(field, request, model_admin)

            # adapted from field.get_choices(...)
            if field.choices is not None:
                return list(field.choices)
            rel_model = field.remote_field.model
            choice_func = operator.attrgetter(
                field.remote_field.get_related_field().attname
                if hasattr(field.remote_field, 'get_related_field')
                else 'pk'
            )
            qs = rel_model._default_manager.complex_filter(additional_filter).order_by(*ordering)
            if select_related is not None:
                qs = qs.select_related(*select_related)
            return [
                (choice_func(x), str(x)) for x in qs
            ]

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


def has_free_places_filter():
    class Wrapper(admin.SimpleListFilter):
        title = 'free places'
        parameter_name = 'has_free_places'

        def lookups(self, request, model_admin):
            return (
                ('1', _('Has free places')),
                ('0', _('Group is full')),
            )

        def queryset(self, request, queryset):
            # enroll_count field was added using qs.annotate, see get_queryset() in groupAdmin
            if self.value() == '1':
                return queryset.filter(capacity__gt=F('enroll_count'))
            if self.value() == '0':
                return queryset.filter(capacity__lte=F('enroll_count'))
            return queryset

    return Wrapper
