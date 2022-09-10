from django.shortcuts import get_object_or_404
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from api.crud.crud_attendance import (
    toggle_has_QR,
    get_detailed_hours, get_detailed_hours_and_self,
)
from api.permissions import (
    IsStudent, IsTrainer, IsStaff,
)
from api.serializers import (
    get_error_serializer,
    TrainingHourSerializer, EmptySerializer,
    HasQRSerializer,
)
from api.serializers.profile import GenderSerializer
from sport.models import Semester, Student, Group


@swagger_auto_schema(
    method="POST",
    responses={
        status.HTTP_200_OK: HasQRSerializer,
    }
)
@api_view(["POST"])
@permission_classes([IsStudent])
def toggle_QR_presence(request, **kwargs):
    """
    Toggles has_QR status
    """
    student = request.user.student
    toggle_has_QR(student)
    serializer = HasQRSerializer(student)
    return Response(serializer.data)


@swagger_auto_schema(
    method="POST",
    request_body=GenderSerializer,
    responses={
        status.HTTP_200_OK: EmptySerializer,
    }
)
@api_view(["POST"])
@permission_classes([IsStaff])
def change_gender(request, **kwargs):
    serializer = GenderSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    print(serializer.validated_data['student_id'])

    student = Student.objects.get(user_id=serializer.validated_data['student_id'])
    student.gender = serializer.validated_data['gender']
    student.save()

    return Response({})


@swagger_auto_schema(
    method="GET",
    responses={
        status.HTTP_200_OK: TrainingHourSerializer(many=True),
        status.HTTP_404_NOT_FOUND: get_error_serializer(
            "training_history",
            error_code=404,
            error_description="Not found",
        )
    }
)
@api_view(["GET"])
@permission_classes([IsStudent])
# TODO: Replace on get_history_with_self
def get_history(request, semester_id: int, **kwargs):
    """
    Get student's trainings per_semester
    """
    semester = get_object_or_404(Semester, pk=semester_id)
    student = request.user  # user.pk == user.student.pk
    return Response({
        "trainings": list(map(
            lambda g: {
                **g,
                "timestamp": timezone.localtime(g["timestamp"]).strftime("%b %d %H:%M"),
            },
            get_detailed_hours(student, semester)
        ))
    })

@swagger_auto_schema(
    method="GET",
    responses={
        status.HTTP_200_OK: TrainingHourSerializer(many=True),
        status.HTTP_404_NOT_FOUND: get_error_serializer(
            "training_history",
            error_code=404,
            error_description="Not found",
        )
    }
)
@api_view(["GET"])
@permission_classes([IsStudent])
def get_history_with_self(request, semester_id: int, **kwargs):
    """
    Get student's trainings per_semester
    """
    semester = get_object_or_404(Semester, pk=semester_id)
    student = request.user  # user.pk == user.student.pk
    return Response({
        "trainings": list(map(
            lambda g: {
                **g,
                "group": g["group"] if g["group_id"] < 0 else Group.objects.get(pk=g["group_id"]).to_frontend_name(),
                "timestamp": timezone.localtime(g["timestamp"]).strftime("%b %d %H:%M"),
            },
            get_detailed_hours_and_self(student, semester)
        ))
    })
