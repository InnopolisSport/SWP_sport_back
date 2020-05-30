from django.contrib import admin


def custom_titled_filter(title, filter_class=admin.RelatedFieldListFilter):
    class Wrapper(filter_class):
        def __new__(cls, *args, **kwargs):
            instance = filter_class.create(*args, **kwargs)
            instance.title = title
            return instance

    return Wrapper


def get_inline(model_class, inline_class=admin.TabularInline, **kwargs):
    class Inline(inline_class):
        model = model_class
        extra = kwargs.get("extra", 3)
        ordering = kwargs.get("ordering")
        autocomplete_fields = kwargs.get("autocomplete_fields", ())

    return Inline
