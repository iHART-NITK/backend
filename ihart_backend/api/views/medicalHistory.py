from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated,IsAdminUser
from django.views.decorators.csrf import csrf_exempt

from ..models import MedicalHistory, User
from .serializers import MedicalHistorySerializer

non_admin_staff = []

def perms(request):
    user = User.objects.get(id = request.user.id)
    if user.user_type in non_admin_staff:
        return False
    return True

@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def medicalHistories(request):
    if not perms(request):
        return Response("Not Autherized to access Medical Histories.",status=401)
    data = MedicalHistory.objects.all()
    serializer = MedicalHistorySerializer(data, many=True)
    return Response(serializer.data)


@csrf_exempt
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
        if request.method == 'POST':
            serializer = MedicalHistorySerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
            return Response(serializer.data)
        else:
            return Response("Medical History not found!",status = 404)