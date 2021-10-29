'''
Prescription Views Module
Contains views to perform CRUD operations and specialized operations on Prescription opbjects
'''
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import APIException

from django.core.exceptions import ObjectDoesNotExist

from ..models import Prescription, User, Diagnosis, Appointment
from ..serializers import PrescriptionSerializer
from .auth import perms


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def prescriptions(request):
    '''
    REST endpoint to fetch all prescriptions
    '''
    if not perms(request):
        return Response("Not Authorized to access prescriptions.", status=401)
    data = Prescription.objects.all()
    serializer = PrescriptionSerializer(data, many=True)
    return Response(serializer.data)


@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def prescription(request, pk):
    '''
    REST endpoint to fetch, update or delete a specific prescription
    '''
    if request.user.id != pk and not perms(request):
        return Response("Not Authorized to access prescription.", status=401)
    try:
        data = Prescription.objects.get(id=pk)
        if request.method == 'GET':
            serializer = PrescriptionSerializer(data, many=False)
            return Response(serializer.data)
        if request.method == 'POST':
            serializer = PrescriptionSerializer(
                instance=data, data=request.data)
            if serializer.is_valid():
                serializer.save()
            return Response(serializer.data)
        if request.method == 'DELETE':
            data.delete()
            return Response("Prescription deleted successfully!", status=200)
    except ObjectDoesNotExist:
        return Response("Prescription not found!", status=404)
    except APIException:
        return Response("Invalid data submitted!", status=401)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create(request):
    '''
    REST endpoint to create a new prescription object
    '''
    serializer = PrescriptionSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def prescriptionsByUser(request, pk):
    '''
    REST endpoint to fetch all prescriptions of a particular user
    '''
    if request.user.id != pk and not perms(request):
        return Response(
            "Not Authorized to access Prescriptions.",
            status=401)
    try:
        user = User.objects.get(id=pk)
        appointments = Appointment.objects.filter(user=user)
        diagnoses = Diagnosis.objects.filter(appointment__in=appointments)
        data = Prescription.objects.filter(diagnosis__in=diagnoses)
        serializer = PrescriptionSerializer(data, many=True)
        return Response(serializer.data)
    except ObjectDoesNotExist:
        return Response("User not found", status=404)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def prescriptionsByUserAppointment(request, pk, a_pk):
    '''
    REST endpoint to get all prescriptions for a user's appointment
    '''
    if request.user.id != pk and not perms(request):
        return Response(
            "Not Authorized to access Prescriptions.",
            status=401)
    try:
        appointment = Appointment.objects.get(id=a_pk)
        diagnoses = Diagnosis.objects.filter(appointment=appointment)
        data = Prescription.objects.filter(
            diagnosis__in=diagnoses).order_by('diagnosis')
        serializer = PrescriptionSerializer(data, many=True)
        return Response(serializer.data)
    except ObjectDoesNotExist:
        return Response("User not found", status=404)
