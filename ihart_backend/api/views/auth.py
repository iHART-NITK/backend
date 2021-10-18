from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .serializers import UserSerializer
from ..models import User


@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        # Create new user
        user = serializer.create(validated_data=request.data)
        token = Token.objects.create(user=user)

        # Generate the response
        response = {
            "Authorization": f"Token {token.key}",
            "id": user.id
        }
        response.update(serializer.data)
        return Response(response)
    else:
        return Response({
            "error": True,
            "error_msg": "Invalid details"
        })


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
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
