from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from django.views.decorators.csrf import csrf_exempt

from ..models import Emergency
from .serializers import UserSerializer

@api_view(['GET'])
def listApis(request):
    # Describe all API routes
    routes = [
        {
            "endpoint": "/api/list-apis/",
            "methods": "GET",
            "body": None,
            "description": "List all accessible API endpoints",
            "is_authenticated": False
        },
        {
            "endpoint": "/api/register/",
            "methods": "POST",
            "body": "username, password, email, first_name, last_name",
            "description": "Registers a new user and generates an auth token for the user",
            "is_authenticated": False
        },
        {
            "endpoint": "/api/token-auth/",
            "methods": "POST",
            "body": "username, password",
            "description": "Verifies a user's credentials and returns the auth token associated with the user if credentials are valid",
            "is_authenticated": False
        },
        {
            "endpoint": "/api/test/",
            "methods": "GET",
            "body": None,
            "description": "Test API that requires authentication",
            "is_authenticated": True
        },
        {
            "endpoint": "/api/emergency/locations",
            "methods": "GET",
            "body": None,
            "description": "Test API that requires authentication",
            "is_authenticated": True
        }
    ]

    return Response(routes)

@csrf_exempt
@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        # Create new user
        user = serializer.create(validated_data=request.data)
        token = Token.objects.create(user=user)

        # Generate the response
        response = {"Authorization": f"Token {token.key}"}
        response.update(serializer.data)
        return Response(response)
    else:
        return Response({
            "error": True,
            "error_msg": "Invalid details"
        })

@csrf_exempt
@api_view(['GET'])
def emergency_choices(request):
    obj = Emergency.objects.first()
    return Response({f"{str(obj.LOCATION_CHOICES)}"})