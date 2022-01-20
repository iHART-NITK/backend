'''
Inventory Views Module
Contains views to perform CRUD operations and specialized operations on Inventory objects
'''
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated

from django.core.exceptions import ObjectDoesNotExist

from ..models import Inventory
from ..serializers import InventorySerializer
from .auth import perms


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def inventories(request):
    '''
    REST endpoint to fetch all inventory objects
    '''
    if not perms(request):
        return Response({
            "error_msg": "You do not have permission to perform this action."
        }, status=401)
    data = Inventory.objects.all()
    serializer = InventorySerializer(data, many=True)
    return Response(serializer.data)


@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def inventory(request, pk):
    '''
    REST endpoint to fetch, update or delete a specific inventory object
    '''
    if request.user.id != pk and not perms(request):
        return Response({
            "error_msg": "You do not have permission to perform this action."
        }, status=401)
    try:
        data = Inventory.objects.get(id=pk)
        if request.method == 'GET':
            serializer = InventorySerializer(data, many=False)
            return Response(serializer.data)
        if request.method == 'POST':
            serializer = InventorySerializer(instance=data, data=request.data)
            if serializer.is_valid():
                serializer.save()
            return Response(serializer.data)
        if request.method == 'DELETE':
            data.delete()
            return Response("Inventory deleted successfully!", status=200)
    except ObjectDoesNotExist:
        return Response({
            "error_msg": "Inventory does not exist."
        }, status=404)
    except APIException:
        return Response({
            "error_msg": "Incorrect details entered."
        }, status=401)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create(request):
    '''
    REST endpoint to create an inventory object
    '''
    serializer = InventorySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)
