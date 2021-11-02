'''
Auth Views Module
Contains all functions to register and verify the authenticity of a user
'''
import re

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated

from django.core.exceptions import ObjectDoesNotExist

from ..serializers import UserSerializer
from ..models import User

non_admin_staff = []


def perms(request):
    '''
    Helper function to verify if a user belongs to the admin staff of HCC
    '''
    user = User.objects.get(id=request.user.id)
    if user.user_type in non_admin_staff:
        return False
    return True


def checkUserType(email):
    '''
    Helper function to verify the user type based on email address
    This functionality can be avoided by using IRIS OAuth
    '''
    username = email.split('@')[0]
    domain = email.split('@')[-1]
    if domain != "nitk.edu.in":
        return None
    rollNumber = username.split('.')[-1]
    if re.match('[1-9][0-9][0-9][a-z]{2}[0-9]{3}', rollNumber):
        return "Stu"
    return "Fac"


@api_view(['POST'])
def register(request):
    '''
    REST endpoint to register a new user and store their information in our database
    '''
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        # Create new user
        user = serializer.create(validated_data=serializer.data)
        token = Token.objects.create(user=user)

        # Generate the response
        response = {
            "token": token.key,
            "id": user.id
        }
        response.update(serializer.data)
        return Response(response)
    print(serializer.errors, "\n\n")
    return Response({
        "error": True,
        "error_msg": "Invalid details"
    }, status=403)


@api_view(['POST'])
def verifyIfRegistered(request):
    '''
    REST endpoint to verify an incoming login request
    '''
    email = request.data['email']
    userType = checkUserType(email)
    if userType is None:
        return Response({
            "error": True,
            "error_msg": "User is not from NITK Domain!"
        }, status=403)
    try:
        user = User.objects.get(email=email)
        if request.data['customer_id'] == user.customer_id:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                "verified": True,
                "token": token.key,
                "id": user.id,
                "user_type": userType
            })
        return Response({
            "error": True,
            "error_msg": "Invalid Login Credentials. \
                If you think this is an issue, contact the HCC Admin."
        }, status=403)
    except ObjectDoesNotExist:
        return Response({
            "verified": False
        }, status=202)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def verifyToken(request):
    '''
    REST endpoint to verify an authentication token value
    '''
    if request.user.id == int(request.POST['id']):
        return Response(True, status=200)
    return Response(False, status=403)


class CustomAuthToken(ObtainAuthToken):
    '''
    REST endpoint to log a user into the application
    (might not even be used, need to verify in the frontend)
    '''

    def post(self, request, *args, **kwargs):
        '''
        Function to handle a POST request to the endpoint
        '''
        serializer = self.serializer_class(
            data=request.data, context={
                'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'id': user.id,
        })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    '''
    REST endpoint to log out a user by deleting their token from the database
    '''
    try:
        Token.objects.get(user=request.user).delete()
        return Response({"logged_out": True}, status=200)
    except:
        return Response({
            "error": True,
            "error_msg": "Could not log the user out successfully!"
        }, status=500)
    
