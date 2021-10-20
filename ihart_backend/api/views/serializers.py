from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from ..models import User, Inventory, Emergency, MedicalHistory, Schedule, Appointment, Diagnosis, Prescription, Transaction


class UserSerializer(serializers.ModelSerializer):
    user_type = serializers.CharField(source='get_user_type_display')
    gender = serializers.CharField(source='get_gender_display')
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
            'phone',
            'user_type',
            'gender'
        )
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=['username', 'email']
            )
        ]


class MedicalHistorySerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='get_category_display')

    class Meta:
        model = MedicalHistory
        fields = (
            'id',
            'user',
            'category',
            'description'
        )


class ScheduleSerializer(serializers.ModelSerializer):
    day = serializers.CharField(source='get_day_display')
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
    status = serializers.CharField(source='get_status_display')
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


class EmergencySerializer(serializers.ModelSerializer):
    location = serializers.CharField(source='get_location_display')
    status = serializers.CharField(source='get_status_display')
    class Meta:
        model = Emergency
        fields = (
            'user',
            'reason',
            'location',
            'status'
        )


class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = (
            'id',
            'prescription',
            'units'
        )


class InventorySerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='get_category_display')
    class Meta:
        model = Inventory
        fields = (
            'id',
            'name',
            'units',
            'category',
            'cost_per_unit'
        )
