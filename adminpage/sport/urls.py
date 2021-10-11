from django.urls import path, re_path
from django.contrib.admin.views.decorators import staff_member_required

from .views import *

urlpatterns = [
    path('', login_redirect, name="login"),
    path('profile/', profile_view, name='profile'),
    path('category/', category_view, name='category'),
    path(
        'calendar/sport/<int:sport_id>',
        calendar_view,
        name="sport_schedule_calendar"
    ),
    path(
        'calendar/extrasport',
        calendar_view_without_sport,
        name="extrasport_schedule_calendar"
    ),
    path(
        'form/meg_group',
        process_med_group_form,
        name="process_med_group_form"
    ),
    re_path(
        r'dashboard/(?P<path>.*)$',
        staff_member_required(GraphanaProxyView.as_view()),
        name='grafana-dashboard'
    ),
]
