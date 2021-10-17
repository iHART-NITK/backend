from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated,IsAdminUser

from ..models import Inventory
from .serializers import InventorySerializer
from .auth import perms

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def inventories(request):
    if not perms(request):
        return Response("Not Authorized to access inventories.",status=401)
    data = Inventory.objects.all()
    serializer = InventorySerializer(data, many=True)
    return Response(serializer.data)

@api_view(['GET','POST','DELETE'])
@permission_classes([IsAuthenticated])
def inventory(request,pk):
    if request.user.id != pk and not perms(request):
        return Response("Not Autherized to access inventory.",status=401)
    data = Inventory.objects.get(id = pk)
    if data:
        if request.method == 'GET':
            serializer = InventorySerializer(data, many=False)
            return Response(serializer.data)
        if not perms(request):
            return Response("Not Autherized to edit Inventory.",status=401)
        if request.method == 'POST':
            serializer = InventorySerializer(instance = data, data = request.data)
            if serializer.is_valid():
                serializer.save()
            return Response(serializer.data)
        elif request.method == 'DELETE':
            data.delete()
            return Response("Inventory deleted successfully!",status = 200)
    else:
        return Response("Inventory not found!",status = 404)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create(request):
    serializer = InventorySerializer(data = request.data)
    if serializer.is_valid():
        serializer.save()
        print('valid serializer')
    return Response(serializer.data)