'''
Schedule Views Module
Contains views to perform CRUD Operations and specialized operations on Schedule objects
'''
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated

from django.core.exceptions import ObjectDoesNotExist

from ..models import Schedule, User
from ..serializers import ScheduleSerializer
from .auth import perms


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def schedules(request):
    '''
    REST endpoint to fetch all schedules
    '''
    if not perms(request):
        return Response("Not Authorized to access Schedules.", status=401)
    data = Schedule.objects.all()
    serializer = ScheduleSerializer(data, many=True)
    return Response(serializer.data)


@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def schedule(request, pk):
    '''
    REST endpoint to fetch, update or delete a specific schedule
    '''
    if request.user.id != pk and not perms(request):
        return Response("Not Authorized to access schedule.", status=401)
    try:
        data = Schedule.objects.get(id=pk)
        if request.method == 'GET':
            serializer = ScheduleSerializer(data, many=False)
            return Response(serializer.data)
        if request.method == 'POST':
            serializer = ScheduleSerializer(instance=data, data=request.data)
            if serializer.is_valid():
                serializer.save()
            return Response(serializer.data)
        if request.method == 'DELETE':
            data.delete()
            return Response("Schedule deleted successfully!", status=200)
    except ObjectDoesNotExist:
        return Response("Schedule not found!", status=404)
    except APIException:
        return Response("Invalid data submitted!")


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create(request):
    '''
    REST endpoint to create a new schedule
    '''
    serializer = ScheduleSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def schedulesByUser(request, pk):
    '''
    REST endpoint to get all schedules for a particular user
    '''
    if request.user.id != pk and not perms(request):
        return Response(
            "Not Authorized to access Schedules.",
            status=401)
    try:
        user = User.objects.get(id=pk)
        data = Schedule.objects.filter(user=user)
        serializer = ScheduleSerializer(data, many=True)
        return Response(serializer.data)
    except ObjectDoesNotExist:
        return Response("User not found", status=404)
