from django.contrib import admin

def custom_titled_filter(title, filterClass=admin.RelatedFieldListFilter):
    class Wrapper(filterClass):
        def __new__(cls, *args, **kwargs):
            instance = filterClass.create(*args, **kwargs)
            instance.title = title
            return instance
    return Wrapper