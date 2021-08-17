from django.conf import settings


def js_version(request):
    return {'JS_VERSION': settings.JS_VERSION}