import re
import threading
from datetime import datetime

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

from api.crud import get_ongoing_semester, get_student_hours, get_negative_hours
from api.permissions import IsStudent
from api.serializers import (
    SelfSportReportUploadSerializer,
    EmptySerializer,
    ErrorSerializer,
    error_detail,
)
from api.serializers.self_sport_report import SelfSportTypes, ActivitySerializer, ParsedActivitySerializer
from api.views.utils import parse_strava_activity_info, parse_training_peaks_activity_info, parse_activity_app_name, parse_self_sport_reports
from sport.models import SelfSportType, SelfSportReport


class SelfSportErrors:
    NO_CURRENT_SEMESTER = (
        7, "You can submit self-sport only during semester"
    )
    MEDICAL_DISALLOWANCE = (
        6, "You can't submit self-sport reports "
           "unless you pass a medical checkup"
    )
    MAX_NUMBER_SELFSPORT = (
        5, "You can't submit self-sport report, because you have max number of self sport"
    )
    INVALID_LINK = (
        4, "You can't submit link submitted previously or link is invalid."
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
        status.HTTP_403_FORBIDDEN: ErrorSerializer
    }
)
@api_view(["POST"])
@permission_classes([IsStudent])
@parser_classes([MultiPartParser])
def self_sport_upload(request, **kwargs):
    # TODO Remove after the frontend is updated
    data = request.data.dict()
    # data.pop('parsed_data')

    current_time = datetime.now()
    semester_start = datetime.combine(get_ongoing_semester().start, datetime.min.time())
    semester_end = datetime.combine(get_ongoing_semester().end, datetime.max.time())
    if not semester_start <= current_time <= semester_end:
        return Response(status=status.HTTP_403_FORBIDDEN, data=error_detail(*SelfSportErrors.NO_CURRENT_SEMESTER))

    serializer = SelfSportReportUploadSerializer(data=data)
    url = serializer.initial_data['link']
    app_name = parse_activity_app_name(url)
    if app_name is None or SelfSportReport.objects.filter(link=url).exists():
        return Response(status=status.HTTP_400_BAD_REQUEST, data=error_detail(*SelfSportErrors.INVALID_LINK))

    student = request.user  # user.pk == user.student.pk
    if request.user.student.medical_group_id < settings.SELFSPORT_MINIMUM_MEDICAL_GROUP_ID:
        return Response(status=status.HTTP_400_BAD_REQUEST, data=error_detail(*SelfSportErrors.MEDICAL_DISALLOWANCE))

    hours_info = get_student_hours(student.id)
    neg_hours = get_negative_hours(student.id, hours_info)
    if (hours_info['ongoing_semester']['hours_self_not_debt'] >= 10
            and not student.has_perm('sport.more_than_10_hours_of_self_sport')):
        return Response(status=status.HTTP_400_BAD_REQUEST, data=error_detail(*SelfSportErrors.MAX_NUMBER_SELFSPORT))

    debt = neg_hours < 0
    serializer.is_valid(raise_exception=True)
    serializer.save(semester=get_ongoing_semester(), student_id=student.pk, debt=debt)

    # Check whether the self sport reports are being parsed at the current moment
    for thread in threading.enumerate():
        if thread.name == 'self_sport_report_parser':
            break
    else:
        thread = threading.Thread(target=parse_self_sport_reports, name='self_sport_report_parser', daemon=True)
        thread.start()

    return Response({})
