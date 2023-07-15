from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

@api_view(["GET"])
def test_endp(request, **kwargs):
    return Response("Test zaebis")
