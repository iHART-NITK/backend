from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated, IsAdminUser

from ..models import Appointment, User
from .serializers import AppointmentSerializer, MedicalHistorySerializer
from .auth import perms


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def appointments(request):
    if not perms(request):
        return Response("Not Autherized to access Appointments.", status=401)
    data = Appointment.objects.all()
    serializer = MedicalHistorySerializer(data, many=True)
    return Response(serializer.data)


@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def appointment(request, pk):
    if request.user.id != pk and not perms(request):
        return Response("Not Autherized to access Appointment.", status=401)
    try:
        data = Appointment.objects.get(id=pk)
        # accessing appointment info
        if request.method == 'GET':
            serializer = AppointmentSerializer(data, many=False)
            return Response(serializer.data)
        if not perms(request):
            return Response("Not Autherized to edit Appointments.", status=401)
        # altering appointment info
        if request.method == 'POST':
            serializer = AppointmentSerializer(
                instance=data, data=request.data)
            if serializer.is_valid():
                serializer.save()
            return Response(serializer.data)
        # deleting appointment info
        elif request.method == 'DELETE':
            data.delete()
            return Response("Appointment deleted successfully!", status=200)
    except:
        return Response("Appointment not found!", status=404)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create(request):
    serializer = AppointmentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def appointmentsByUser(request, pk):
    if request.user.id != pk and not perms(request):
        return Response(
            "Not Autherized to access Appointments.",
            status=401)
    try:
        user = User.objects.get(id=pk)
        data = Appointment.objects.filter(user=user)
        serializer = AppointmentSerializer(data, many=True)
        return Response(serializer.data)
    except:
        return Response("User not found", status=404)
