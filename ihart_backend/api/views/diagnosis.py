from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated,IsAdminUser
from django.views.decorators.csrf import csrf_exempt

from ..models import Diagnosis,User
from .serializers import DiagnosisSerializer
from .auth import perms

@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def diagnoses(request):
    if not perms(request):
        return Response("Not Autherized to access diagnoses.",status=401)
    data = Diagnosis.objects.all()
    serializer = DiagnosisSerializer(data, many=True)
    return Response(serializer.data)


@csrf_exempt
@api_view(['GET','POST','DELETE'])
@permission_classes([IsAuthenticated])
def diagnosis(request,pk):
    if request.user.id != pk and not perms(request,pk):
        return Response("Not Autherized to access Diagnosis.",status=401)
    data = Diagnosis.objects.get(id = pk)
    if data:
        if request.method == 'GET':
            serializer = DiagnosisSerializer(data, many=False)
            return Response(serializer.data)
        if not perms(request,pk):
            return Response("Not Autherized to edit Diagnosis.",status=401)
        if request.method == 'POST':
            serializer = DiagnosisSerializer(instance = data, data = request.data)
            if serializer.is_valid():
                serializer.save()
            return Response(serializer.data)
        elif request.method == 'DELETE':
            data.delete()
            return Response("DIagnosis deleted successfully!",status = 200)
    else:
        return Response("Diagnosis not found!",status = 404)

@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create(request):
    serializer = DiagnosisSerializer(data = request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)