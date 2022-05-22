from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from api.permissions import IsStudent
from api.serializers import NotFoundSerializer
from api.serializers.training import NewTrainingInfoSerializer, NewTrainingInfoStudentSerializer
from sport.models import Training, Student


@swagger_auto_schema(
    method="GET",
    responses={
        status.HTTP_200_OK: NewTrainingInfoStudentSerializer(),
        status.HTTP_404_NOT_FOUND: NotFoundSerializer(),
    }
)
@api_view(["GET"])
@permission_classes([IsStudent])
def training_info(request, training_id, **kwargs):
    training = get_object_or_404(Training, pk=training_id)
    student: Student = request.user.student
    checked_in = training.checkins.filter(student=student).exists()
    can_check_in = student.medical_group in training.group.allowed_medical_groups.all()
    return Response(NewTrainingInfoStudentSerializer({
        'training': training,
        'can_check_in': can_check_in,
        'checked_in': checked_in
    }).data)
