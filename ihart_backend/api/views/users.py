from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated,IsAdminUser
from django.views.decorators.csrf import csrf_exempt

from ..models import User
from .serializers import UserSerializer

non_admin_staff = []

def perms(request):
    user = User.objects.get(id = request.user.id)
    if user.user_type in non_admin_staff:
        return False
    return True

@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def users(request):
    if not perms(request):
        return Response("Not Autherized to access profiles.",status=401)
    users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


@csrf_exempt
@api_view(['GET','POST','DELETE'])
@permission_classes([IsAuthenticated])
def user(request,pk):
    if request.user.id != pk and not perms(request,pk):
        return Response("Not Autherized to access profile.",status=401)
    user = User.objects.get(id = pk)
    if request.method == 'GET':
        serializer = UserSerializer(user, many=False)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = UserSerializer(instance = user, data = request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)
    elif request.method == 'DELETE':
        user.delete()
        return Response("User deleted successfully!",status = 200)
