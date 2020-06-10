from django.urls import path
from django.contrib.auth.views import LoginView

from .views import *
from .views.reference import reference_upload_view

urlpatterns = [
    path('', LoginView.as_view(
        redirect_authenticated_user=True,
    ), name="login"),

    path('profile/', profile_view, name='profile'),
    path('category/', category_view, name='category'),
    path('calendar/sport/<int:sport_id>', calendar_view, name="sport_schedule_calendar"),
    path('reference/upload', reference_upload_view, name='reference_upload_view')
]
