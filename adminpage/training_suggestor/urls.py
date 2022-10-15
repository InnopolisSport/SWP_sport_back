from django.urls import path
from .views import suggest, get_poll, add_poll_result, get_poll_result, get_telegram_users

urlpatterns = [
    path('tg_users', get_telegram_users),
    path('suggest', suggest),
    path('poll/<str:name>', get_poll),
    path('poll_result', add_poll_result),
    path('poll_result/<str:poll_name>', get_poll_result),
]
