from drf_yasg.openapi import Parameter, IN_QUERY
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.crud import get_ongoing_semester
from api.serializers.semester import SemesterSerializer

from sport.models import Semester


@swagger_auto_schema(
    method='GET',
    manual_parameters=[Parameter('current', IN_QUERY, type='bool')],
    operation_description='Get semesters.',
    responses={status.HTTP_200_OK: SemesterSerializer(many=True)}
)
@api_view(['GET'])
def get_semester(request, **kwargs):
    current = request.query_params.get('current', False)
    current = True if current == 'true' else False

    if current:
        data = [SemesterSerializer(get_ongoing_semester()).data]
        return Response(status=status.HTTP_200_OK, data=data)
    else:
        data = [SemesterSerializer(obj).data for obj in Semester.objects.all()]
        return Response(status=status.HTTP_200_OK, data=data)
