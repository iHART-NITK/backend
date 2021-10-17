from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated,IsAdminUser

from ..models import MedicalHistory, User
from .serializers import MedicalHistorySerializer
from .auth import perms

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def medicalHistories(request):
    if not perms(request):
        return Response("Not Autherized to access Medical Histories.",status=401)
    data = MedicalHistory.objects.all()
    serializer = MedicalHistorySerializer(data, many=True)
    return Response(serializer.data)


@api_view(['GET','POST','DELETE'])
@permission_classes([IsAuthenticated])
def medicalHistory(request,pk):
    if request.user.id != pk and not perms(request,pk):
        return Response("Not Autherized to access Medical History.",status=401)
    data = MedicalHistory.objects.filter(id = pk)
    if data:
        if request.method == 'GET':
            serializer = MedicalHistorySerializer(data, many=True)
            return Response(serializer.data)
        if not perms(request,pk):
            return Response("Not Autherized to edit Medical History.",status=401)
        if request.method == 'POST':
            serializer = MedicalHistorySerializer(instance = data, data = request.data)
            if serializer.is_valid():
                serializer.save()
            return Response(serializer.data)
        elif request.method == 'DELETE':
            data.delete()
            return Response("Medical history deleted successfully!",status = 200)
    else:
        return Response("Medical History not found!",status = 404)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create(request):
    serializer = MedicalHistorySerializer(data = request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def medicalHistoriesByUser(request,pk):
    if request.user.id != pk and not perms(request,pk):
        return Response("Not Autherized to access Medical Histories.",status=401)
    user = User.objects.get(id = pk)
    if user :
        data = MedicalHistory.objects.filter(user = user)
        serializer = MedicalHistorySerializer(data, many=True)
        return Response(serializer.data)
    else:
        return Response("User not found",status=404)