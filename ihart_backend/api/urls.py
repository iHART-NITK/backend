from django.urls import path
from rest_framework.authtoken import views as restViews

from . import views

urlpatterns = [
    path('list-apis/', views.listApis, name="list-apis"),
    path('register/', views.register, name="register"),
    path('token-auth/', restViews.obtain_auth_token, name="token-auth"),
    path('test/', views.test, name="test")
]