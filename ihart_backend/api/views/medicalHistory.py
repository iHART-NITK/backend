'''
Medical History Views Module
Contains views to perform CRUD operations and specialized operations on Medical History objects
'''
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render

from hashlib import sha256

from ..models import MedicalHistory, User
from ..serializers import MedicalHistorySerializer, UserSerializer
from .auth import perms


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def medicalHistories(request):
    '''
    REST endpoint to fetch all medical histories
    '''
    if not perms(request):
        return Response(
            "Not Authorized to access Medical Histories.",
            status=401)
    data = MedicalHistory.objects.all()
    serializer = MedicalHistorySerializer(data, many=True)
    return Response(serializer.data)


@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def medicalHistory(request, pk):
    '''
    REST endpoint to fetch the medical history of a specific user
    '''
    if request.user.id != pk and not perms(request):
        return Response(
            "Not Authorized to access Medical History.",
            status=401)
    try:
        data = MedicalHistory.objects.filter(id=pk)
        if request.method == 'GET':
            serializer = MedicalHistorySerializer(data, many=True)
            return Response(serializer.data)
        if request.method == 'POST':
            serializer = MedicalHistorySerializer(
                instance=data, data=request.data)
            if serializer.is_valid():
                serializer.save()
            return Response(serializer.data)
        if request.method == 'DELETE':
            data.delete()
            return Response(
                "Medical history deleted successfully!",
                status=200)
    except ObjectDoesNotExist:
        return Response("Medical History not found!", status=404)
    except APIException:
        return Response("Invalid data sent!", status=401)




@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create(request):
    '''
    REST endpoint to create a medical history
    '''
    token = request.headers.get('Authorization').split()[1]
    data = request.data.copy()
    data["user"] = Token.objects.get(key=token).user.id
    serializer = MedicalHistorySerializer(data=data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def medicalHistoriesByUser(request, pk):
    '''
    REST endpoint to fetch all medical history objects of a particular user
    '''
    if request.user.id != pk and not perms(request):
        return Response(
            "Not Authorized to access Medical Histories.",
            status=401)
    try:
        user = User.objects.get(id=pk)
        data = MedicalHistory.objects.filter(user=user)
        serializer = MedicalHistorySerializer(data, many=True)
        return Response(serializer.data)
    except ObjectDoesNotExist:
        return Response("User not found", status=404)

@api_view(['GET'])
def medicalHistoryByUserHtml(request, pk):
    user = User.objects.get(id=pk)
    hashedToken = request.GET.get("token")
    token = Token.objects.get(user=user).key
    shaHash = sha256()
    shaHash.update(token.encode('utf-8'))
    if (hashedToken != shaHash.hexdigest()):
        return Response({
            "error": True,
            "error_msg": "Hashes do not match!"
        }, status=403)

    data = MedicalHistory.objects.filter(user=user)
    dataSerialized = MedicalHistorySerializer(data, many=True)
    userSerialized = UserSerializer(user)
    return render(request, "api/medical-history.html", {
        "user": userSerialized.data,
        "data": dataSerialized.data
    })
