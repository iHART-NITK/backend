from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from django.views.decorators.csrf import csrf_exempt

from ./../models import Prescription,User
from .serializers import PrescriptionSerializer

non_admin_staff = []

def perms(request):
    user = User.objects.get(id = request.user.id)
    if user.user_type in non_admin_staff:
        return False
    return True

@csrf_exempt
@api_view(['GET','DELETE'])
@permission_classes([IsAuthenticated])
def prescriptions(request):
    if not perms(request):
        return Response("Not Autherized to access prescriptions.",status=401)
    data = Prescription.objects.all()
    if request.method == 'GET':
        serializer = PrescriptionSerializer(data, many=True)
        return Response(serializer.data)
    elif request.method == 'DELETE':
        count = data.delete()
        return Response("'message': '{} prescriptions were deleted successfully!'.format(count[0])",status = 200)


@csrf_exempt
@api_view(['GET','POST','DELETE'])
@permission_classes([IsAuthenticated])
def prescription(request,pk):
    if request.user.id != pk and not perms(request,pk):
        return Response("Not Autherized to access prescription.",status=401)
    data = Prescription.objects.get(id = pk)
    if data:
        if request.method == 'GET':
            serializer = PrescriptionSerializer(data, many=False)
            return Response(serializer.data)
        if not perms(request,pk):
            return Response("Not Autherized to edit Prescription.",status=401)
        if request.method == 'POST':
            serializer = PrescriptionSerializer(instance = data, data = request.data)
            if serializer.is_valid():
                serializer.save()
            return Response(serializer.data)
        elif request.method == 'DELETE':
            data.delete()
            return Response("Prescription deleted successfully!",status = 200)
    else:
        if request.method == 'POST':
            serializer = PrescriptionSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
            return Response(serializer.data)
        else:
            return Response("Prescription not found!",status = 404)