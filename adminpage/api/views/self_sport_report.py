from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import (
    parser_classes,
    permission_classes,
    api_view,
)
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from api.crud import get_ongoing_semester
from api.permissions import IsStudent
from api.serializers import (
    SelfSportReportUploadSerializer,
    EmptySerializer,
    ErrorSerializer,
)
from api.views.utils import process_image


class SelfSportErrors:
    pass


@swagger_auto_schema(
    method="POST",
    operation_description="One of image or link required",
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

    image = None
    link = serializer.validated_data.get('link', None)

    if 'image' in serializer.validated_data:
        image, error = process_image(serializer.validated_data['image'])
        if error is not None:
            return error

    student = request.user  # user.pk == user.student.pk
    serializer.save(
        image=image,
        link=link,
        semester=get_ongoing_semester(),
        student_id=student.pk
    )

    return Response({})
