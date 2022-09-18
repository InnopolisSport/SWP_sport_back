from django.urls import path
from .views import suggest, get_poll, add_poll_result

urlpatterns = [
    path('suggest', suggest),
    path('poll/<str:name>', get_poll),
    path('poll_result', add_poll_result),
]
