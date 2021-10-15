from django.urls import path
from rest_framework.authtoken import views as restViews

from ./views import views, users , medicalHistory , schedule , appointment ,diagnosis

urlpatterns = [
    path('list-apis/', views.listApis, name="list-apis"),
    path('register/', views.register, name="register"),
    path('token-auth/', restViews.obtain_auth_token, name="token-auth"),
    path('user/', users.users, name="users"),
    path('user/<int:pk>/', users.user, name="user")
    path('medical-history/', medicalHistory.medicalHistories, name="medical-histories"),
    path('medical-history/<int:pk>/', medicalHistory.medicalHistory, name="medical-history")
    path('schedule/', schedule.schedules, name="schedules"),
    path('schedule/<int:pk>/', schedule.schedule, name="schedule")
    path('appointment/', appointment.appointments, name="appointments"),
    path('appointment/<int:pk>/', appointment.appointment, name="appointment")
    path('diagnosis/', diagnosis.diagnoses, name="diagnoses"),
    path('diagnosis/<int:pk>/', diagnosis.diagnosis, name="diagnosis")
    path('prescription/', prescription.prescriptions, name="prescriptions"),
    path('prescription/<int:pk>/', prescription.prescription, name="prescription")
]