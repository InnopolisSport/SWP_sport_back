from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from api.crud import get_group_info, get_sports
from api.permissions import IsStudent
from api.serializers import GroupInfoSerializer, NotFoundSerializer, SportsSerializer
from sport.models import Group, Schedule


@swagger_auto_schema(
    method="GET",
    responses={
        status.HTTP_200_OK: GroupInfoSerializer,
        status.HTTP_404_NOT_FOUND: NotFoundSerializer,
    }
)
@api_view(["GET"])
@permission_classes([IsStudent])
def group_info_view(request, group_id, **kwargs):
    student = request.user  # user.pk == user.student.pk
    get_object_or_404(Group, pk=group_id)
    group_info = get_group_info(group_id, student)
    group_schedule = Schedule.objects.filter(group_id=group_id).all()
    group_info.update({"schedule": group_schedule})
    serializer = GroupInfoSerializer(group_info)
    return Response(serializer.data)


@swagger_auto_schema(
    method="GET",
    responses={
        status.HTTP_200_OK: SportsSerializer,
        status.HTTP_404_NOT_FOUND: NotFoundSerializer,
    }
)
@api_view(["GET"])
@permission_classes([IsStudent])
def sports_view(request, **kwargs):
    print(get_sports())
    serializer = SportsSerializer({'sports': get_sports()})
    return Response(serializer.data)
