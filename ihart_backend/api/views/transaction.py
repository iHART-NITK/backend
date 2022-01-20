'''
Transaction Views Module
Contains views to perform CRUD operations and specialized operations on Transaction objects
'''
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import APIException

from django.core.exceptions import ObjectDoesNotExist

from ..models import Transaction, User, Appointment, Prescription, Diagnosis
from ..serializers import TransactionSerializer
from .auth import perms


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def transactions(request):
    '''
    REST endpoint to fetch all transactions
    '''
    if not perms(request):
        return Response({
            "error_msg": "You do not have permission to perform this action."
        }, status=401)
    data = Transaction.objects.all()
    serializer = TransactionSerializer(data, many=True)
    return Response(serializer.data)


@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def transaction(request, pk):
    '''
    REST endpoint to fetch, update or delete a specific transaction
    '''
    if request.user.id != pk and not perms(request):
        return Response({
            "error_msg": "You do not have permission to perform this action."
        }, status=401)
    try:
        data = Transaction.objects.get(id=pk)
        if request.method == 'GET':
            serializer = TransactionSerializer(data, many=False)
            return Response(serializer.data)
        if request.method == 'POST':
            serializer = TransactionSerializer(
                instance=data, data=request.data)
            if serializer.is_valid():
                serializer.save()
            return Response(serializer.data)
        if request.method == 'DELETE':
            data.delete()
            return Response("Transaction deleted successfully!", status=200)
    except ObjectDoesNotExist:
        return Response({
            "error_msg": "Transaction does not exist."
        }, status=404)
    except APIException:
        return Response({
            "error_msg": "Incorrect details entered."
        }, status=401)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create(request):
    '''
    REST endpoint to create a new transaction
    '''
    serializer = TransactionSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def transactionsByUser(request, pk):
    '''
    REST endpoint to fetch all transactions for a specific user
    '''
    if request.user.id != pk and not perms(request):
        return Response({
            "error_msg": "You do not have permission to perform this action."
        }, status=401)
    try:
        user = User.objects.get(id=pk)
        appointments = Appointment.objects.filter(user=user)
        diagnoses = Diagnosis.objects.filter(appointment__in=appointments)
        prescription = Prescription.objects.filter(diagnosis__in=diagnoses)
        data = Transaction.objects.filter(prescription__in=prescription)
        serializer = TransactionSerializer(data, many=True)
        return Response(serializer.data)
    except ObjectDoesNotExist:
        return Response({
            "error_msg": "User does not exist."
        }, status=404)
