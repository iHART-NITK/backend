from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated, IsAdminUser

from ..models import Schedule, User
from .serializers import ScheduleSerializer
from .auth import perms


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def schedules(request):
    if not perms(request):
        return Response("Not Autherized to access Schedules.", status=401)
    data = Schedule.objects.all()
    serializer = ScheduleSerializer(data, many=True)
    return Response(serializer.data)


@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def schedule(request, pk):
    if request.user.id != pk and not perms(request):
        return Response("Not Autherized to access schedule.", status=401)
    data = Schedule.objects.get(id=pk)
    if data:
        if request.method == 'GET':
            serializer = ScheduleSerializer(data, many=False)
            return Response(serializer.data)
        elif request.method == 'POST':
            serializer = ScheduleSerializer(instance=data, data=request.data)
            if serializer.is_valid():
                serializer.save()
            return Response(serializer.data)
        elif request.method == 'DELETE':
            data.delete()
            return Response("Schedule deleted successfully!", status=200)
    else:
        return Response("Schedule not found!", status=404)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create(request):
    serializer = ScheduleSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def schedulesByUser(request, pk):
    if request.user.id != pk and not perms(request):
        return Response(
            "Not Autherized to access Schedules.",
            status=401)
    user = User.objects.get(id=pk)
    if user:
        data = Schedule.objects.filter(user = user)
        serializer = ScheduleSerializer(data, many=True)
        return Response(serializer.data)
    else:
        return Response("User not found", status=404)