from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from ..models import User, Inventory, Emergency, MedicalHistory, Schedule, Appointment, Diagnosis, Prescription


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source="get_full_name", read_only=True)
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'phone',
            'user_type',
            'full_name'
        ]
        read_only_fields = ['full_name']
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=['username', 'email']
            )
        ]
    def get_full_name(self, obj):
        user = User.objects.get(username=obj["username"])
        
        if user.middle_name != "":
            return f"{user.first_name} {user.middle_name} {user.last_name}"
        else:
            return f"{user.first_name} {user.last_name}"


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


class EmergencySerializer(serializers.ModelSerializer):

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
        model = Prescription
        fields = (
            'id',
            'user',
            'inventory',
            'prescription',
            'units'
        )


class InventorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Inventory
        fields = (
            'id',
            'name',
            'units',
            'category',
            'cost_per_unit'
        )
