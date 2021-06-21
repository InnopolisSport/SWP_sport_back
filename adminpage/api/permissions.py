from django.conf import settings

from rest_framework import permissions

from django.contrib.auth import get_user_model

from sport.models import Student


class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        if str(Student.objects.filter(user=get_user_model().objects.filter(email=request.user.email)[0])[0].student_status) == 'Normal' and hasattr(request.user, 'student'):
            return True
        return False


class IsTrainer(permissions.BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'trainer')
