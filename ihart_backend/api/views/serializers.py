from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from ..models import User, Inventory, Emergency, MedicalHistory, Schedule, Appointment, Diagnosis, Prescription, Transaction


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source="get_full_name", read_only=True)
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
            'phone',
            'user_type',
            'full_name',
            'gender',
            'customer_id'
        )
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
    doctor_name = serializers.SerializerMethodField()
    has_prescriptions = serializers.SerializerMethodField()

    def get_doctor_name(self, obj):
        doc = obj.schedule.user
        return doc.first_name + ' ' + doc.last_name
        # return doc.first_name + " " + doc.last_name
    
    def get_has_prescriptions(self, obj):
        diags = Diagnosis.objects.filter(appointment=obj)
        return Prescription.objects.filter(diagnosis__in=diags).exists()

    class Meta:
        model = Appointment
        fields = (
            'id',
            'schedule',
            'user',
            'doctor_name',
            'date',
            'start_time',
            'status',
            'create_time',
            'has_prescriptions'
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
    diagnosis = serializers.CharField(source='diagnosis.diagnosis', read_only=True)
    inventory = serializers.CharField(source='inventory.name', read_only=True)
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
    def create(self, obj):
        newObj = Emergency.objects.create(user=obj['user'], reason=obj['reason'], location=obj['get_location_display'], status=obj['get_status_display'])
        return newObj
    
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
