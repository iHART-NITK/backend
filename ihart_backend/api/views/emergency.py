'''
Emergency Views Module
Contains all views to perfom CRUD operations and specific operations on Emergency objects
'''
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

from django.core.exceptions import ObjectDoesNotExist

from ..models import Emergency, User
from ..serializers import EmergencySerializer
from .auth import perms


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def locations(request):
    '''
    REST Endpoint to fetch all possible emergency locations
    This function can be deprecated by using geolocation services
    '''
    if not perms(request):
        return Response("Not Authorized to access Locations.", status=401)
    data = Emergency.LOCATION_CHOICES
    # return Response(converters.(data, {}))
    locationHash = {}
    for abbr, loc in data:
        locationHash.setdefault(abbr, loc)
    return Response(locationHash)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def location(request, pk):
    '''
    REST Endpoint to fetch a particular location
    '''
    if not perms(request):
        return Response("Not Authorized to access Locations.", status=401)
    data = Emergency.LOCATION_CHOICES[pk]
    return Response(data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create(request):
    '''
    REST endpoint to create an emergency
    '''
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
    '''
    REST endpoint to fetch all emergencies by a specific user
    '''
    if request.user.id != pk and not perms(request):
        return Response(
            "Not Authorized to access Emergencies.",
            status=401)
    try:
        user = User.objects.get(id=pk)
        data = Emergency.objects.filter(user=user)
        serializer = EmergencySerializer(data, many=True)
        return Response(serializer.data)
    except ObjectDoesNotExist:
        return Response("User not found", status=404)
