'''
Document Views Module
Contains all views to perform CRUD operations and specialized operations on Document objects.
'''
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import APIException

from django.core.exceptions import ObjectDoesNotExist
from django.http import FileResponse

from ..serializers import DocumentSerializer
from ..models import Document
from .auth import perms


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def documents(request):
    '''
    REST Framework view to fetch all documents
    '''
    if not perms(request):
        return Response({
            "error_msg": "You do not have permission to perform this action."
        }, status=401)
    data = Document.objects.all()
    serializer = DocumentSerializer(data, many=True)
    return Response(serializer.data)


@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def document(request, pk):
    '''
    REST endpoint to fetch, update or delete a specific appointment
    '''
    if not perms(request):
        return Response({
            "error_msg": "You do not have permission to perform this action."
        }, status=401)
    try:
        data = Document.objects.get(id=pk)
        # accessing document file
        if request.method == 'GET':
            file = data.file
            return FileResponse(file)
        # TODO: Add Document upload functionality
        # if request.method == 'POST':
        #     serializer = AppointmentSerializer(
        #         instance=data, data=request.data)
        #     if serializer.is_valid():
        #         serializer.save()
        #     return Response(serializer.data)
        # # deleting appointment info
        # if request.method == 'DELETE':
        #     data.delete()
        #     return Response("Appointment deleted successfully!", status=200)
    except ObjectDoesNotExist:
        return Response("Document not found!", status=404)
    except APIException:
        return Response("Invalid Data entered!", status=401)


# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def create(request):
#     '''
#     REST endpoint to create a new appointment
#     '''
#     serializer = AppointmentSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#     return Response(serializer.data)
