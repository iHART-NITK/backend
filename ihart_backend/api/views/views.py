from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated,IsAdminUser

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
        },
        {
            "endpoint": "/api/<resource>",
            "methods": "GET",
            "body": None,
            "description": "Retrieve all objects of model",
            "is_authenticated": True
        },
        {
            "endpoint": "/api/<resource>/<int:pk>",
            "methods": "GET,POST,DELETE",
            "body": "depends on method and resource",
            "description": "interact with individual object of resource/model with that id",
            "is_authenticated": True
        },
        {
            "endpoint": "/api/<resource>/create",
            "methods": "POST",
            "body": "depends on model/resource",
            "description": "Create a new object in the model( user model does not have this endpoint)",
            "is_authenticated": True
        },
        {
            "endpoint": "/api/user/<int:pk>/<resource>",
            "methods": "GET",
            "body": None,
            "description": "Retrieve all objects of model with user having id = pk",
            "is_authenticated": True
        },
    ]

    return Response(routes)