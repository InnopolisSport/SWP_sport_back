from django.contrib import admin


def custom_titled_filter(title, filterClass=admin.RelatedFieldListFilter):
    class Wrapper(filterClass):
        def __new__(cls, *args, **kwargs):
            instance = filterClass.create(*args, **kwargs)
            instance.title = title
            return instance

    return Wrapper


def get_inline(model_class, inline_class=admin.TabularInline, **kwargs):
    class Inline(inline_class):
        model = model_class
        extra = kwargs.get("extra", 3)
    return Inline
