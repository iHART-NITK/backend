from django.urls import path
from rest_framework.authtoken import views as restViews


from .views import views, users, medicalHistory, schedule, appointment, diagnosis, prescription, emergency, auth, transaction, inventory

urlpatterns = [
    path('list-apis/', views.listApis, name="list-apis"),
    path('register/', auth.register, name="register"),
    path('token-auth/', auth.CustomAuthToken.as_view(), name="token-auth"),

    path('user/', users.users, name="users"),
    path('user/<int:pk>/', users.user, name="user"),

    path('medical-history/', medicalHistory.medicalHistories, name="medical-histories"),
    path('medical-history/<int:pk>/', medicalHistory.medicalHistory, name="medical-history"),
    path('medical-history/create/',medicalHistory.create, name="medical-history-create"),
    path('user/<int:pk>/medical-history/',medicalHistory.medicalHistoriesByUser, name="medical-histories-by-user"),

    path('schedule/', schedule.schedules, name="schedules"),
    path('schedule/<int:pk>/', schedule.schedule, name="schedule"),
    path('schedule/create/',schedule.create, name="schedule-create"),

    path('appointment/', appointment.appointments, name="appointments"),
    path('appointment/<int:pk>/', appointment.appointment, name="appointment"),
    path('appointment/create',appointment.create, name="appointment-create"),

    path('diagnosis/', diagnosis.diagnoses, name="diagnoses"),
    path('diagnosis/<int:pk>/', diagnosis.diagnosis, name="diagnosis"),
    path('diagnosis/create',diagnosis.create, name="diagnosis-create"),
    
    path('prescription/', prescription.prescriptions, name="prescriptions"),
    path('prescription/<int:pk>/', prescription.prescription, name="prescription"),
    path('prescription/create',prescription.create, name="prescription-create"),
    
    path('emergency/create/', emergency.create, name="emergency-create"),
    path('emergency/locations/', emergency.locations, name="locations"),
    path('emergency/location/<int:pk>/', emergency.location, name="location"),

    path('transaction/', transaction.transactions, name="transactions"),
    path('transaction/<int:pk>/', transaction.transaction, name="transaction"),
    path('transaction/create/',transaction.create, name="transaction-create"),

    path('inventory/', inventory.inventories, name="inventories"),
    path('inventory/<int:pk>/', inventory.inventory, name="inventory"),
    path('inventory/create/',inventory.create, name="inventory-create"),
]