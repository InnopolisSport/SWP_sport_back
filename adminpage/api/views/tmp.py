from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.serializers import TmpSerializer


# You can also use rest_framework.viewsets.ViewSet
# and annotate each method
@swagger_auto_schema(
    method="GET",
    responses={
        status.HTTP_200_OK: TmpSerializer,
    }
)
@api_view(["GET"])
def test(request, **kwargs):
    """
    Some comment to function

    Detailed description
    """
    return Response({"ping": "pong"})
