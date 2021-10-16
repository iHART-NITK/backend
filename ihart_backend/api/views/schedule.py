from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated,IsAdminUser
from django.views.decorators.csrf import csrf_exempt

from ..models import Schedule, User
from .serializers import ScheduleSerializer

non_admin_staff = []

def perms(request):
    user = User.objects.get(id = request.user.id)
    if user.user_type in non_admin_staff:
        return False
    return True

@csrf_exempt
@api_view(['GET','DELETE'])
@permission_classes([IsAuthenticated])
def schedules(request):
    if not perms(request):
        return Response("Not Autherized to access Schedules.",status=401)
    data = Schedule.objects.all()
    if request.method == 'GET':
        serializer = ScheduleSerializer(data, many=True)
        return Response(serializer.data)
    elif request.method == 'DELETE':
        count = data.delete()
        return Response("'message': '{} Schedules were deleted successfully!'.format(count[0])",status = 200)


@csrf_exempt
@api_view(['GET','POST','DELETE'])
@permission_classes([IsAuthenticated])
def schedule(request,pk):
    if request.user.id != pk and not perms(request,pk):
        return Response("Not Autherized to access schedule.",status=401)
    data = Schedule.objects.get(id = pk)
    if data:
        if request.method == 'GET':
            serializer = ScheduleSerializer(data, many=False)
            return Response(serializer.data)
        elif request.method == 'POST':
            serializer = ScheduleSerializer(instance = data, data = request.data)
            if serializer.is_valid():
                serializer.save()
            return Response(serializer.data)
        elif request.method == 'DELETE':
            data.delete()
            return Response("Schedule deleted successfully!",status = 200)
    else:
        if request.method == 'POST':
            serializer = ScheduleSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
            return Response(serializer.data)
        else:
            return Response("Schedule not found!",status = 404)