from django.urls import path, re_path
from django.contrib.admin.views.decorators import staff_member_required

from bot.views import auth_view

urlpatterns = [
    path('auth/', auth_view, name="login"),
]
