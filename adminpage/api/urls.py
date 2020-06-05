from django.conf.urls import url

from adminpage.swagger import schema_view
from django.urls import path

from api.views import (
    tmp,
    profile,
    enroll,
    group,
    training,
)

urlpatterns = [
    path(r"test/", tmp.test),
    # profile
    path(r"profile/sick/toggle", profile.toggle_sick),
    path(r"profile/history/<int:semester_id>", profile.get_history),

    # enroll
    path(r"enrollment/enroll", enroll.enroll),
    path(r"enrollment/unenroll", enroll.unenroll),

    # group
    path(r"group/<int:group_id>", group.group_info),

    # training
    path(r"training/<int:training_id>", training.training_info),
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
