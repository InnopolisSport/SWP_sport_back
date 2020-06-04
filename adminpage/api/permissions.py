from django.conf import settings

from rest_framework import permissions


class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and \
                request.user.groups.filter(
                    verbose_name=settings.STUDENT_GROUP_VERBOSE_NAME
                ):
            return True
        return False


class IsTrainer(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and \
                request.user.groups.filter(
                    verbose_name=settings.TRAINER_GROUP_VERBOSE_NAME
                ):
            return True
        return False
