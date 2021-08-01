from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from api.crud import get_attended_training_info
from api.permissions import IsStudent
from api.serializers import TrainingInfoSerializer, NotFoundSerializer
from sport.models import Training


@swagger_auto_schema(
    method="GET",
    responses={
        status.HTTP_200_OK: TrainingInfoSerializer,
        status.HTTP_404_NOT_FOUND: NotFoundSerializer,
    }
)
@api_view(["GET"])
@permission_classes([IsStudent])
def training_info(request, training_id, **kwargs):
    student = request.user  # user.pk == user.student.pk
    get_object_or_404(Training, pk=training_id)
    return Response(get_attended_training_info(training_id, student))
