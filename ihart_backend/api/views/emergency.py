from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authtoken.models import Token

from ..models import Emergency, User
from .serializers import EmergencySerializer
from .auth import perms


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def locations(request):
    if not perms(request):
        return Response("Not Autherized to access Locations.", status=401)
    data = Emergency.LOCATION_CHOICES
    # return Response(converters.(data, {}))
    location_hash = {}
    for abbr, loc in data:
        location_hash.setdefault(abbr, loc)
    return Response(location_hash)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def location(request, pk):
    if not perms(request):
        return Response("Not Autherized to access Locations.", status=401)
    data = Emergency.LOCATION_CHOICES[pk]
    return Response(data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create(request):
    token = request.headers.get('Authorization').split()[1]
    data = request.data.copy()
    data["user"] = Token.objects.get(key=token).user.id
    serializer = EmergencySerializer(data=data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def emergenciesByUser(request, pk):
    if request.user.id != pk and not perms(request):
            return Response(
            "Not Autherized to access Emergencies.",
            status=401)
    try:
        user = User.objects.get(id=pk)
        data = Emergency.objects.filter(user=user)
        serializer = EmergencySerializer(data, many=True)
        return Response(serializer.data)
    except:
        return Response("User not found", status=404)
