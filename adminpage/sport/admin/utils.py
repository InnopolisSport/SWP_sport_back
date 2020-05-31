from django.contrib import admin


def custom_titled_filter(title, filter_class=admin.RelatedFieldListFilter):
    class Wrapper(filter_class):
        def __new__(cls, *args, **kwargs):
            instance = filter_class.create(*args, **kwargs)
            instance.title = title
            return instance

    return Wrapper
