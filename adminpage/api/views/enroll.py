from django.db import transaction, InternalError, IntegrityError
from django.shortcuts import get_object_or_404
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from api.crud import (
    unenroll_student,
    get_ongoing_semester,
    enroll_student_to_primary_group,
    enroll_student_to_secondary_group,
)
from api.permissions import IsStudent
from api.serializers import (
    EnrollSerializer,
    error_detail,
    EmptySerializer,
    NotFoundSerializer,
    ErrorSerializer,
)
from sport.models import Group


class EnrollErrors:
    GROUP_IS_FULL = (2, "Group you chosen is full")
    TOO_MUCH_SECONDARY = (3, "You have too much secondary groups")
    DOUBLE_ENROLL = (4, "You can't enroll to a group you have already enrolled to")
    PRIMARY_UNENROLL = (5, "Can't unenroll from primary group")
    MEDICAL_DISALLOWANCE = (6, "You can't enroll to the group due to your medical group")


@swagger_auto_schema(
    method="POST",
    request_body=EnrollSerializer,
    responses={
        status.HTTP_200_OK: EmptySerializer,
        status.HTTP_404_NOT_FOUND: NotFoundSerializer,
        status.HTTP_400_BAD_REQUEST: ErrorSerializer,
    },
)
@api_view(["POST"])
@permission_classes([IsStudent])
@transaction.atomic
def enroll(request, **kwargs):
    """
    Enroll student

    error codes:
    2 - Group you chosen is full
    3 - You have too much secondary groups
    4 - You can't enroll to a group you have already enrolled to
    6 - Enroll with insufficient medical group
    """
    serializer = EnrollSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    group = get_object_or_404(
        Group,
        pk=serializer.validated_data["group_id"]
    )
    student = request.user.student
    current_semester = get_ongoing_semester()
    if student.medical_group < group.minimum_medical_group:
        return Response(
            status=status.HTTP_400_BAD_REQUEST,
            data=error_detail(*EnrollErrors.MEDICAL_DISALLOWANCE)
        )
    if timezone.localdate() <= current_semester.choice_deadline:
        try:
            enroll_student_to_primary_group(group, student)
        except InternalError:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data=error_detail(*EnrollErrors.GROUP_IS_FULL)
            )
    else:
        try:
            enroll_student_to_secondary_group(group, student)
        except IntegrityError:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data=error_detail(
                    *EnrollErrors.DOUBLE_ENROLL
                )
            )
        except InternalError as e:
            if "too much groups" in str(e):
                return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data=error_detail(
                        *EnrollErrors.TOO_MUCH_SECONDARY
                    )
                )
            else:
                return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data=error_detail(
                        *EnrollErrors.GROUP_IS_FULL
                    )
                )
    return Response({})


@swagger_auto_schema(
    method="POST",
    request_body=EnrollSerializer,
    responses={
        status.HTTP_200_OK: EmptySerializer,
        status.HTTP_404_NOT_FOUND: NotFoundSerializer,
        status.HTTP_400_BAD_REQUEST: ErrorSerializer,
    },
)
@api_view(["POST"])
@permission_classes([IsStudent])
@transaction.atomic
def unenroll(request, **kwargs):
    """
    Unenroll student

    Error codes:
    5 - Can't unenroll from primary group
    """
    serializer = EnrollSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    group = get_object_or_404(
        Group,
        pk=serializer.validated_data["group_id"]
    )
    student = request.user.student
    removed_count = unenroll_student(group, student)
    if removed_count == 0:
        return Response(
            status=status.HTTP_400_BAD_REQUEST,
            data=error_detail(
                *EnrollErrors.PRIMARY_UNENROLL
            )
        )
    return Response({})
