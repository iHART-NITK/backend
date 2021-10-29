'''
Appointment Views Module
Contains all views to perform CRUD operations and specialized operations on Appointment objects.
'''
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import APIException

from django.core.exceptions import ObjectDoesNotExist


from ..models import Appointment, User
from ..serializers import AppointmentSerializer, MedicalHistorySerializer
from .auth import perms


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def appointments(request):
    '''
    REST Framework view to fetch all appointments
    '''
    if not perms(request):
        return Response("Not Authorized to access Appointments.", status=401)
    data = Appointment.objects.all()
    serializer = MedicalHistorySerializer(data, many=True)
    return Response(serializer.data)


@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def appointment(request, pk):
    '''
    REST endpoint to fetch, update or delete a specific appointment
    '''
    if request.user.id != pk and not perms(request):
        return Response("Not Authorized to access Appointment.", status=401)
    try:
        data = Appointment.objects.get(id=pk)
        # accessing appointment info
        if request.method == 'GET':
            serializer = AppointmentSerializer(data, many=False)
            return Response(serializer.data)
        # altering appointment info
        if request.method == 'POST':
            serializer = AppointmentSerializer(
                instance=data, data=request.data)
            if serializer.is_valid():
                serializer.save()
            return Response(serializer.data)
        # deleting appointment info
        if request.method == 'DELETE':
            data.delete()
            return Response("Appointment deleted successfully!", status=200)
    except ObjectDoesNotExist:
        return Response("Appointment not found!", status=404)
    except APIException:
        return Response("Invalid Data entered!", status=401)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create(request):
    '''
    REST endpoint to create a new appointment
    '''
    serializer = AppointmentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def appointmentsByUser(request, pk):
    '''
    REST endpoint to fetch all appointments for a user
    '''
    if request.user.id != pk and not perms(request):
        return Response(
            "Not Authorized to access Appointments.",
            status=401)
    try:
        user = User.objects.get(id=pk)
        data = Appointment.objects.filter(
            user=user).order_by('-date', '-start_time')
        serializer = AppointmentSerializer(data, many=True)
        return Response(serializer.data)
    except ObjectDoesNotExist:
        return Response("User not found", status=404)
