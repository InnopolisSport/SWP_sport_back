from django.conf.urls import url

from adminpage.swagger import schema_view
from django.urls import path

from .views import tmp

urlpatterns = [
    path(r"test/", tmp.test),
]

urlpatterns.extend([
    url(
        r'swagger(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0),
        name='schema-json'
    ),
    url(
        r'swagger/$',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'
    ),
    url(
        r'redoc/$',
        schema_view.with_ui('redoc', cache_timeout=0),
        name='schema-redoc'
    ),
])
