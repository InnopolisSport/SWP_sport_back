from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from api.permissions import IsStudent
from api.serializers import NotFoundSerializer, EmptySerializer, ErrorSerializer, error_detail
from api.serializers.training import NewTrainingInfoSerializer, NewTrainingInfoStudentSerializer
from sport.models import Training, Student, TrainingCheckIn, Attendance


@swagger_auto_schema(
    method="GET",
    responses={
        status.HTTP_200_OK: NewTrainingInfoStudentSerializer(),
        status.HTTP_404_NOT_FOUND: NotFoundSerializer(),
    }
)
@api_view(["GET"])
@permission_classes([IsStudent])
def training_info(request, training_id, **kwargs):
    training = get_object_or_404(Training, pk=training_id)
    student: Student = request.user.student
    checked_in = training.checkins.filter(student=student).exists()
    can_check_in = student.medical_group in training.group.allowed_medical_groups.all()
    try:
        hours = Attendance.objects.get(training=training, student=student).hours
    except Attendance.DoesNotExist:
        hours = None

    return Response(NewTrainingInfoStudentSerializer({
        'training': training,
        'can_check_in': can_check_in,
        'checked_in': checked_in,
        'hours': hours
    }).data)


@swagger_auto_schema(
    method="GET",
    responses={
        status.HTTP_200_OK: EmptySerializer(),
        status.HTTP_404_NOT_FOUND: NotFoundSerializer(),
        status.HTTP_400_BAD_REQUEST: ErrorSerializer(),
    }
)
@api_view(["GET"])
@permission_classes([IsStudent])
def training_checkin(request, training_id, **kwargs):
    student: Student = request.user.student
    try:
        TrainingCheckIn.objects.create(student=student, training_id=training_id)
        return Response()
    except IntegrityError as e:
        if 'is not present in table' in str(e):
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data=NotFoundSerializer({'detail': 'Training not found'}).data
            )
        return Response(
            status=status.HTTP_400_BAD_REQUEST,
            data=error_detail(1, "You already checked in this training")
        )


@swagger_auto_schema(
    method="GET",
    responses={
        status.HTTP_200_OK: EmptySerializer(),
        status.HTTP_404_NOT_FOUND: NotFoundSerializer(),
        status.HTTP_400_BAD_REQUEST: ErrorSerializer(),
    }
)
@api_view(["GET"])
@permission_classes([IsStudent])
def training_cancel_checkin(request, training_id, **kwargs):
    try:
        Training.objects.get(id=training_id)
    except Training.DoesNotExist:
        return Response(
            status=status.HTTP_404_NOT_FOUND,
            data=NotFoundSerializer({'detail': 'Training not found'}).data
        )

    student: Student = request.user.student

    try:
        TrainingCheckIn.objects.get(training_id=training_id, student=student).delete()
        return Response()
    except TrainingCheckIn.DoesNotExist:
        return Response(
            status=status.HTTP_400_BAD_REQUEST,
            data=error_detail(1, "You did not check in this training")
        )
