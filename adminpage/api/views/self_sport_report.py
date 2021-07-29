from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import (
    parser_classes,
    permission_classes,
    api_view,
)
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from api.views import get_student_hours_info
from api.crud import get_ongoing_semester
from api.permissions import IsStudent
from api.serializers import (
    SelfSportReportUploadSerializer,
    EmptySerializer,
    ErrorSerializer,
    error_detail,
)
from api.serializers.self_sport_report import SelfSportTypes
# from api.views.utils import process_image
from sport.models import SelfSportType


class SelfSportErrors:
    MEDICAL_DISALLOWANCE = (
        6, "You can't submit self-sport reports "
           "unless you pass a medical checkup"
    )
    MAX_NUMBER_SELFSPORT = (
        5, "You can't submit self-sport report, because you have max number of self sport"
    )


@swagger_auto_schema(
    method="Get",
    responses={
        status.HTTP_200_OK: SelfSportTypes(many=True),
    }
)
@api_view(["GET"])
def get_self_sport_types(request, **kwargs):
    sport_types = SelfSportType.objects.filter(
        is_active=True
    ).all()
    serializer = SelfSportTypes(sport_types, many=True)
    return Response(serializer.data)


@swagger_auto_schema(
    method="POST",
    operation_description="One link to Strava required (begins with http(s)://)",
    request_body=SelfSportReportUploadSerializer,
    responses={
        status.HTTP_200_OK: EmptySerializer,
        status.HTTP_400_BAD_REQUEST: ErrorSerializer,
    }
)
@api_view(["POST"])
@permission_classes([IsStudent])
@parser_classes([MultiPartParser])
def self_sport_upload(request, **kwargs):
    serializer = SelfSportReportUploadSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    student = request.user  # user.pk == user.student.pk
    if request.user.student.medical_group_id \
            < settings.SELFSPORT_MINIMUM_MEDICAL_GROUP_ID:
        return Response(
            status=400,
            data=error_detail(*SelfSportErrors.MEDICAL_DISALLOWANCE),
        )
    hours_info = get_student_hours_info(student.id)
    hours_cur_sem = hours_info['hours_self_debt_current'] \
                    + hours_info['hours_self_not_debt_current'] \
                    + hours_info['hours_not_self_current']
    hours_last_sem = hours_info['hours_not_self_last'] \
                     + hours_info['hours_self_not_debt_last']
    if hours_info['hours_self_not_debt_current'] >= 10 and not student['user'].has_perm('sport.more_than_10_hours_of_self_sport'):
        return Response(
            status=400,
            data=error_detail(*SelfSportErrors.MAX_NUMBER_SELFSPORT),
        )

    # image = None
    link = serializer.validated_data.get('link', None)

    # if 'image' in serializer.validated_data:
    #     image, error = process_image(serializer.validated_data['image'])
    #     if error is not None:
    #         return error

    serializer.save(
        # image=image,
        link=link,
        semester=get_ongoing_semester(),
        student_id=student.pk,
    )

    return Response({})
