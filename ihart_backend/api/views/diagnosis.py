'''
Diagnosis Views Module
Contains all views to perform CRUD operations and specialized operations on Diagnosis objects
'''
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import APIException
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated

from django.core.exceptions import ObjectDoesNotExist

from ..models import Diagnosis, User, Appointment
from ..serializers import DiagnosisSerializer
from .auth import perms


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def diagnoses(request):
    '''
    REST endpoint to fetch all diagnoses
    '''
    if not perms(request):
        return Response("Not Authorized to access diagnoses.", status=401)
    data = Diagnosis.objects.all()
    serializer = DiagnosisSerializer(data, many=True)
    return Response(serializer.data)


@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def diagnosis(request, pk):
    '''
    REST endpoint to get, update or delete a particular diagnosis
    '''
    if request.user.id != pk and not perms(request):
        return Response("Not Authorized to access Diagnosis.", status=401)
    try:
        data = Diagnosis.objects.get(id=pk)
        if request.method == 'GET':
            serializer = DiagnosisSerializer(data, many=False)
            return Response(serializer.data)
        if request.method == 'POST':
            serializer = DiagnosisSerializer(instance=data, data=request.data)
            if serializer.is_valid():
                serializer.save()
            return Response(serializer.data)
        if request.method == 'DELETE':
            data.delete()
            return Response("DIagnosis deleted successfully!", status=200)
    except ObjectDoesNotExist:
        return Response("Diagnosis not found!", status=404)
    except APIException:
        return Response("Invalid data submitted!", status=401)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create(request):
    '''
    REST endpoint to create a new diagnosis
    '''
    serializer = DiagnosisSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def diagnosesByUser(request, pk):
    '''
    REST endpoint to get all diagnoses for a given user
    '''
    if request.user.id != pk and not perms(request):
        return Response(
            "Not Authorized to access Diagnoses.",
            status=401)
    try:
        user = User.objects.get(id=pk)
        appointments = Appointment.objects.filter(user=user)
        data = Diagnosis.objects.filter(appointment__in=appointments)
        serializer = DiagnosisSerializer(data, many=True)
        return Response(serializer.data)
    except ObjectDoesNotExist:
        return Response("User not found", status=404)
