from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from ..models import Transaction, User , Appointment, Prescription, Diagnosis
from .serializers import TransactionSerializer
from .auth import perms


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def transactions(request):
    if not perms(request):
        return Response("Not Authorized to access transactions.", status=401)
    data = Transaction.objects.all()
    serializer = TransactionSerializer(data, many=True)
    return Response(serializer.data)


@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def transaction(request, pk):
    if request.user.id != pk and not perms(request):
        return Response("Not Autherized to access transaction.", status=401)
    try:
        data = Transaction.objects.get(id=pk)
        if request.method == 'GET':
            serializer = TransactionSerializer(data, many=False)
            return Response(serializer.data)
        if not perms(request):
            return Response("Not Autherized to edit Transaction.", status=401)
        if request.method == 'POST':
            serializer = TransactionSerializer(
                instance=data, data=request.data)
            if serializer.is_valid():
                serializer.save()
            return Response(serializer.data)
        elif request.method == 'DELETE':
            data.delete()
            return Response("Transaction deleted successfully!", status=200)
    except:
        return Response("Transaction not found!", status=404)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create(request):
    serializer = TransactionSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def transactionsByUser(request, pk):
    if request.user.id != pk and not perms(request):
        return Response(
            "Not Autherized to access Transactions.",status=401)
    try:
        user = User.objects.get(id=pk)
        appointments = Appointment.objects.filter(user = user)
        diagnoses = Diagnosis.objects.filter(appointment__in = appointments)
        prescription = Prescription.objects.filter(diagnosis__in = diagnoses)
        data = Transaction.objects.filter(prescription__in = prescription)
        serializer = TransactionSerializer(data, many=True)
        return Response(serializer.data)
    except:
        return Response("User not found", status=404)