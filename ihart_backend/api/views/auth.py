from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated, IsAdminUser

import re

from .serializers import UserSerializer
from ..models import User

def checkUserType(email):
    username = email.split('@')[0]
    domain = email.split('@')[-1]
    if domain != "nitk.edu.in":
        return None
    rollNumber = username.split('.')[-1]
    if re.match('[1-9][0-9][0-9][a-z]{2}[0-9]{3}', rollNumber):
        return "Stu"
    else:
        return "Fac"

@api_view(['POST'])
def register(request):
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
    else:
        print(serializer.errors, "\n\n")
        return Response({
            "error": True,
            "error_msg": "Invalid details"
        }, status=403)

@api_view(['POST'])
def verifyIfRegistered(request):
    email = request.POST['email']
    user_type = checkUserType(email)
    if user_type is None:
        return Response({
            "error": True,
            "error_msg": "User is not from NITK Domain!"
        }, status=403)
    try:
        user = User.objects.get(email=email)
        if request.POST['customer_id'] == user.customer_id:
            # TODO: Change this to only get, using get_or_create only for debugging now
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                "verified": True,
                "token": token.key,
                "id": user.id,
                "user_type": user_type
            })
        else:
            return Response({
                "error": True,
                "error_msg": "Invalid Login Credentials. If you think this is an issue, contact the HCC Admin."
            }, status=403)
    except:
        return Response({
            "verified": False
        }, status=202)


class CustomAuthToken(ObtainAuthToken):

    def post(self, request):
        serializer = self.serializer_class(
            data=request.data, context={
                'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'id': user.id,
        })


non_admin_staff = []


def perms(request):
    user = User.objects.get(id=request.user.id)
    if user.user_type in non_admin_staff:
        return False
    return True
