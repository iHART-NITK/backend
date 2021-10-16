from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.views.decorators.csrf import csrf_exempt

from ..models import Emergency, User

non_admin_staff = []

def perms(request):
    user = User.objects.get(id = request.user.id)
    if user.user_type in non_admin_staff:
        return False
    return True

@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def locations(request):
    if not perms(request):
        return Response("Not Autherized to access Locations.",status=401)
    data = Emergency.LOCATION_CHOICES
    # return Response(converters.(data, {}))
    location_hash = {}
    for abbr, loc in data:
        location_hash.setdefault(abbr, loc)
    return Response(str(location_hash))

@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def location(request, pk):
    if not perms(request):
        return Response("Not Autherized to access Locations.",status=401)
    data = Emergency.LOCATION_CHOICES[pk]
    return Response(data)