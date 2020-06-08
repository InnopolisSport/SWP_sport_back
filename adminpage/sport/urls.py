from django.urls import path
from django.contrib.auth.views import LoginView

from .views import *

urlpatterns = [
    path('login/', LoginView.as_view(
        redirect_authenticated_user=True,
    )),

    path('profile/', profile_view, name='profile'),
    path('category/', category_view, name='category'),
    path('calendar/sport/<int:sport_id>', calendar_view, name="sport_schedule_calendar"),
]
