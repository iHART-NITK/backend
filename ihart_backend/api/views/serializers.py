from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from ..models import User, Inventory, Emergency, MedicalHistory, Schedule, Appointment, Diagnosis, Prescription

class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
        )
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=['username', 'email']
            )
        ]

class MedicalHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = MedicalHistory
        fields = (
            'id',
            'user',
            'category',
            'description'
        )

class ScheduleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Schedule
        fields = (
            'id',
            'user',
            'entry_time',
            'exit_time', 
            'day'
        )

class AppointmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Appointment
        fields = (
            'id',
            'schedule',
            'user',
            'start_time',
            'status',
            'create_time'
        )

class DiagnosisSerializer(serializers.ModelSerializer):

    class Meta:
        model = Diagnosis
        fields = (
            'id',
            'appointment',
            'diagnosis'
        )

class PrescriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Prescription
        fields = (
            'id',
            'diagnosis', 
            'inventory', 
            'dosage', 
            'medicine_units'
        )