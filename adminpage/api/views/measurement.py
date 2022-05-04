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
    MeasurementPost,
    Measurement as MeasurementSerializer,
    MeasurementResult,
    MeasurementResults,
    EmptySerializer,
    NotFoundSerializer,
    ErrorSerializer, SuggestionQuerySerializer, SuggestionSerializer
)

from sport.models import Group, Measurement, MeasurementSession, MeasurementResult, Student


@swagger_auto_schema(
    method="GET",
    query_serializer=MeasurementSerializer(many=True),
    responses={
        status.HTTP_200_OK: MeasurementResults,
    }
)
@api_view(["GET"])
def get_measurements(request, **kwargs):
    measurements = Measurement.objects.all()
    result = []
    for measurement in measurements:
        result.append({"name": measurement.name, "value_unit": measurement.value_unit})
    return Response(result)


@swagger_auto_schema(
    method="GET",
    query_serializer=MeasurementResults,
    responses={
        status.HTTP_200_OK: MeasurementResults,
    }
)
@api_view(["GET"])
@permission_classes([IsStudent])
def get_results(request, **kwargs):
    session = MeasurementSession.objects.filter(student=request.user.student)
    if not len(session):
        return Response([])
    else:
        session = session[0]
    results = MeasurementResult.objects.filter(session=session)
    response = {}
    if not len(results):
        return Response({"code": "There is no results"})
    for result in results:
        _result = {
            'measurement': result.measurement.name,
            'unit': result.measurement.value_unit,
            'value': result.value,
            'approved': result.session.approved,
            'date': result.session.date,
        }
        if response.get(result.session.semester.name, None) is None:
            response[result.session.semester.name] = [_result]
        else:
            response[result.session.semester.name].append(_result)
    return Response([{"semester": key, "result": response[key]} for key in response.keys()])


@swagger_auto_schema(
    method="POST",
    request_body=MeasurementPost,
    responses={
        status.HTTP_404_NOT_FOUND: NotFoundSerializer,
        status.HTTP_400_BAD_REQUEST: ErrorSerializer,
    },
)
@api_view(["POST"])
def post_student_measurement(request, **kwargs):
    approved = False
    if hasattr(request.user, 'trainer'):
        approved = True
    student = request.user.student if approved is False else Student.objects.get(user_id=request.data['student_id'])
    measurement = Measurement.objects.filter(id=request.data['measurement_id'])
    if not len(measurement):
        return Response({})
    else:
        measurement = measurement[0]
    session = MeasurementSession.objects.get_or_create(student=student, approved=approved,
                                                       date=datetime.datetime.today(),
                                                       semester=get_ongoing_semester())[0]

    result = MeasurementResult.objects.get_or_create(measurement=measurement, session=session)
    result[0].value = request.data['value']
    result[0].save()
    return Response({'result_id': result[0].id})
