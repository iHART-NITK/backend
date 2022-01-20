'''
User Views Module
Contains views to perform CRUD operations and specialized operations on User objects
'''
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated

from django.core.exceptions import ObjectDoesNotExist

from ..models import User
from ..serializers import UserSerializer
from .auth import perms


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def users(request):
    '''
    REST endpoint to fetch all users
    '''
    if not perms(request):
        return Response({
            "error_msg": "You do not have permission to perform this action."
        }, status=401)
    allUsers = User.objects.all()
    serializer = UserSerializer(allUsers, many=True)
    return Response(serializer.data)


@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def user(request, pk):
    '''
    REST endpoint to fetch, update or delete a particular user
    '''
    if request.user.id != pk and not perms(request):
        return Response({
            "error_msg": "You do not have permission to perform this action."
        }, status=401)
    try:
        getUser = User.objects.get(id=pk)
        if request.method == 'GET':
            serializer = UserSerializer(getUser, many=False)
            return Response(serializer.data)
        elif request.method == 'POST':
            serializer = UserSerializer(instance=getUser, data=request.data)
            if serializer.is_valid():
                serializer.save()
            return Response(serializer.data)
        elif request.method == 'DELETE':
            getUser.delete()
            return Response("User deleted successfully!", status=200)
    except ObjectDoesNotExist:
        return Response({
            "error_msg": "User does not exist."
        }, status=404)
