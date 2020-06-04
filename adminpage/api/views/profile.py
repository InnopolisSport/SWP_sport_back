from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from api.crud.crud_attendance import (
    toggle_illness,
    get_detailed_hours,
)
from api.permissions import (
    IsStudent,
)
from api.serializers import (
    get_error_serializer,
    IsIllSerializer,
    TrainingHourSerializer,
)
from sport.models import Semester


@swagger_auto_schema(
    method="POST",
    responses={
        status.HTTP_200_OK: IsIllSerializer,
    }
)
@api_view(["POST"])
@permission_classes([IsStudent])
def toggle_sick(request, **kwargs):
    """
    Toggle is_sick status
    """
    student = request.user.student
    toggle_illness(student)
    serializer = IsIllSerializer(student)
    return Response(serializer.data)


@swagger_auto_schema(
    method="GET",
    responses={
        status.HTTP_200_OK: TrainingHourSerializer(many=True),
        status.HTTP_404_NOT_FOUND:  get_error_serializer(
            "training_history",
            error_code=404,
            error_description="Not found",
        )
    }
)
@api_view(["GET"])
@permission_classes([IsStudent])
def get_history(request, semester_id: int, **kwargs):
    """
    Get student's trainings per_semester
    """
    semester = get_object_or_404(Semester, pk=semester_id)
    student = request.user.student
    return Response(get_detailed_hours(student, semester))
