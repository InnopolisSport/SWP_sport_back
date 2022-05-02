import datetime
from collections import defaultdict

from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from api.crud import get_ongoing_semester

from api.permissions import (
    IsTrainer, IsStudent,
)

from api.serializers import (
    Measurement,
    MeasurementResult,
    MeasurementSession,
    EmptySerializer,
    NotFoundSerializer,
    ErrorSerializer, SuggestionQuerySerializer, SuggestionSerializer
)

from sport.models import Group, Measurement, MeasurementSession, MeasurementResult, Student


@api_view(["GET"])
def get_measurement(request, **kwargs):
    return Response(Measurement.objects.all())


@swagger_auto_schema(
    method="GET",
    responses={
        status.HTTP_200_OK: MeasurementSession
    }
)
@api_view(["GET"])
def get_sessions(request, **kwargs):
    return Response(MeasurementSession.objects.all())


@api_view(["GET"])
@permission_classes([IsStudent])
def get_results(request, **kwargs):
    session = MeasurementSession.objects.get_or_create(date=datetime.datetime.today(), semester=get_ongoing_semester())
    results = MeasurementResult.objects.filter(session=session)
    response = []
    if len(results) == 0:
        return Response({"code": "There is no such results"})
    for result in results:
        _result = {
            'measurement': result.measurement.name,
            'unit': result.measurement.value_unit,
            'value': result.value,
            'approved': result.session.approved,
            'date': result.session.date,
            'semester': result.session.semester.name
        }
        response.append(_result)
    return Response(response)


@api_view(["POST"])
def post_student_measurement(request, **kwargs):
    approved = False
    if hasattr(request.user, 'trainer'):
        approved = True
    student = request.user.student if approved is False else Student.objects.get(id=request.data.student_id)
    measurement = Measurement.objects.get(name=request.data.measurement_name)
    session = MeasurementSession.objects.get_or_create(student=student, approved=approved,
                                                       date=datetime.datetime.today(),
                                                       semester=get_ongoing_semester())
    result = MeasurementResult.objects.get_or_create(measurement=measurement, session=session)
    result.value = max(result.value, request.data.value)
    result.save()
    return Response({'result_id': result.id})
