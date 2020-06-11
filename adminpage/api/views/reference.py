from django.db import transaction
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from sport.models import Reference
from api.crud import get_ongoing_semester
from api.permissions import IsStudent
from api.serializers import (
    ReferenceUploadSerializer,
    EmptySerializer,
    ErrorSerializer,
    error_detail,
)


class ReferenceErrors:
    TOO_MUCH_UPLOADS_PER_DAY = (123, "Only 1 reference upload per day is allowed")


@swagger_auto_schema(
    method="POST",
    request_body=ReferenceUploadSerializer,
    responses={
        status.HTTP_200_OK: EmptySerializer,
        status.HTTP_400_BAD_REQUEST: ErrorSerializer,
    },
)
@api_view(["POST"])
@permission_classes([IsStudent])
@parser_classes([MultiPartParser])
def reference_upload(request, **kwargs):
    serializer = ReferenceUploadSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    student = request.user.student

    try:
        with transaction.atomic():
            ref = serializer.save(semester=get_ongoing_semester(), student=student)
            count = Reference.objects.filter(student=student, uploaded__date=ref.uploaded.date()).count()
            assert count == 1
    except AssertionError:
        return Response(
            status=status.HTTP_400_BAD_REQUEST,
            data=error_detail(*ReferenceErrors.TOO_MUCH_UPLOADS_PER_DAY)
        )
    return Response({})
