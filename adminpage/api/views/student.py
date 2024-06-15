from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.response import Response
from django.views.decorators.cache import cache_page

from api.crud import get_email_name_like_students, Training, \
    get_students_grades, mark_hours, get_student_last_attended_dates, get_detailed_hours, get_ongoing_semester, \
    get_student_hours, get_negative_hours, better_than, get_email_name_like_students_filtered_by_group
from api.permissions import IsStaff, IsStudent, IsTrainer
from api.serializers import StudentInfoSerializer, AttendanceSerializer ,SuggestionQuerySerializer, SuggestionSerializer, \
    NotFoundSerializer, InbuiltErrorSerializer, \
    TrainingGradesSerializer, AttendanceMarkSerializer, error_detail, \
    BadGradeReportGradeSerializer, BadGradeReport, LastAttendedDatesSerializer, HoursInfoSerializer, HoursInfoFullSerializer
from api.serializers.attendance import BetterThanInfoSerializer
from sport.models import Group, Student, Semester, SelfSportReport, Attendance

User = get_user_model()

@swagger_auto_schema(
    method="GET",
    query_serializer=AttendanceSerializer,
    responses={
        status.HTTP_200_OK: AttendanceSerializer(many=True),
    }
)
@api_view(["GET"])
@permission_classes([IsTrainer])
def attendance(request, **kwargs):
    return Response()



@swagger_auto_schema(
    method="PUT",
    query_serializer=AttendanceSerializer,
    responses={
        status.HTTP_200_OK: AttendanceSerializer(many=True),
    }
)
@api_view(["PUT"])
@permission_classes([IsTrainer])
def attendance_update(request,student_id, attendance_id, **kwargs):
    return Response()




@swagger_auto_schema(
    method="DELETE",
    query_serializer=StudentInfoSerializer,
    responses={
        status.HTTP_200_OK: StudentInfoSerializer(many=True),
    }
)
@api_view(["DELETE"])
@permission_classes([IsTrainer])
def batch_delete(request, **kwargs):
    return Response()