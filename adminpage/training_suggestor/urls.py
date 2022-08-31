from django.urls import path, include
from .views import suggest


urlpatterns = [
    path('suggest', suggest),
]
