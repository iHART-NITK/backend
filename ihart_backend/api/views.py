from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User

# Create your views here.
@login_required(login_url="/login")
def index(request):
    users = User.objects.all()
    user_json = serializers.serialize('json', users)
    return HttpResponse(user_json, content_type="application/json")

# Login view of the web application
def login_view(request):
    # If user tried to access this page by submitting the login form
    if request.method == 'POST':
        # Retrieve the username and password from the POST parameters
        username = request.POST['username']
        password = request.POST['password']

        # Authenticate the user by comparing the username and password to the data available in the database
        # SQL : SELECT * FROM user WHERE username={username} AND password={hash(password)}
        user = authenticate(request, username=username, password=password)

        # If the user exists and the password is valid, login the user and redirect them to the index page
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse(index))
        # If the authenticate function did not return a user, then the input data is invalid
        # Render the login page again with error message
        else:
            return render(request, 'api/login.html', {
                'message': 'Invalid Username or Password.',
            })
    
    # If the user tried to access this page by clicking the login link
    return render(request, 'api/login.html')

# Logout view of the web application
def logout_view(request):
    # Logout the user, and redirect them back to the index page
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):
    pass