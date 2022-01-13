'''
Serializers Module
Contains all the serializers to serialize data into JSON format for REST endpoints
'''
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import *

class UserSerializer(serializers.ModelSerializer):
    '''
    Serializer to serialize User objects
    '''
    full_name = serializers.CharField(source="get_full_name", read_only=True)
    user_type = serializers.CharField(source='get_user_type_display')
    gender = serializers.CharField(source='get_gender_display')
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    class Meta:
        '''
        Meta class to define the Model to use for ModelSerializer
        '''
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
            'customer_id',
            'photo'
        )
        read_only_fields = ['full_name']
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=['username', 'email']
            )
        ]

    def get_full_name(self, obj):
        '''
        Function to generate the user's full name from first/middle/last name
        '''
        user = User.objects.get(username=obj["username"])

        if user.middle_name != "":
            return f"{user.first_name} {user.middle_name} {user.last_name}"
        return f"{user.first_name} {user.last_name}"


# class MedicalHistorySerializer(serializers.ModelSerializer):
#     '''
#     Serializer to serialize Medical History objects
#     '''
#     category = serializers.CharField(source='get_category_display')

#     class Meta:
#         '''
#         Meta class to define the Model to use for ModelSerializer
#         '''
#         model = MedicalHistory
#         fields = (
#             'user',
#             'category',
#             'description'
#         )
class MedicalHistorySerializer(serializers.ModelSerializer):
    '''
    Serializer to serialize Medical History objects
    '''
    def create(self, validated_data):
        newObj = MedicalHistory.objects.create(
            user=validated_data['user'],
            category=validated_data['get_category_display'],
            description=validated_data['description']
            )
        return newObj

    category = serializers.CharField(source='get_category_display')


    class Meta:
        '''
        Meta class to define the Model to use for ModelSerializer
        '''
        model = MedicalHistory
        fields = (
            'user',
            'category',
            'description'
        )


class ScheduleSerializer(serializers.ModelSerializer):
    '''
    Serializer to serialize Schedule objects
    '''
    day = serializers.CharField(source='get_day_display')
    class Meta:
        '''
        Meta class to define the Model to use for ModelSerializer
        '''
        model = Schedule
        fields = (
            'id',
            'user',
            'entry_time',
            'exit_time',
            'day'
        )


class AppointmentSerializer(serializers.ModelSerializer):
    '''
    Serializer to serialize Appointment objects
    '''
    status = serializers.CharField(source='get_status_display')
    doctor_name = serializers.SerializerMethodField()
    has_prescriptions = serializers.SerializerMethodField()

    class Meta:
        '''
        Meta class to define the Model to use for ModelSerializer
        '''
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

    def get_doctor_name(self, obj):
        '''
        Function to get the Doctor's full name from their first/last name
        '''
        doc = obj.schedule.user
        return doc.first_name + ' ' + doc.last_name
        # return doc.first_name + " " + doc.last_name

    def get_has_prescriptions(self, obj):
        '''
        Function to check if prescriptions exist for a given appointment
        '''
        diags = Diagnosis.objects.filter(appointment=obj)
        return Prescription.objects.filter(diagnosis__in=diags).exists()


class DiagnosisSerializer(serializers.ModelSerializer):
    '''
    Serializer to serialize Diagnosis objects
    '''
    class Meta:
        '''
        Meta class to define the Model to use for ModelSerializer
        '''
        model = Diagnosis
        fields = (
            'id',
            'appointment',
            'diagnosis'
        )


class PrescriptionSerializer(serializers.ModelSerializer):
    '''
    Serializer to serialize Prescription objects
    '''
    diagnosis = serializers.CharField(source='diagnosis.diagnosis', read_only=True)
    inventory = serializers.CharField(source='inventory.name', read_only=True)
    class Meta:
        '''
        Meta class to define the Model to use for ModelSerializer
        '''
        model = Prescription
        fields = (
            'id',
            'diagnosis',
            'inventory',
            'dosage',
            'medicine_units'
        )


class EmergencySerializer(serializers.ModelSerializer):
    '''
    Serializer to serialize Emergency objects
    '''
    def create(self, validated_data):
        newObj = Emergency.objects.create(
            user=validated_data['user'],
            reason=validated_data['reason'],
            location=validated_data['get_location_display'],
            status=validated_data['get_status_display']
        )
        return newObj

    location = serializers.CharField(source='get_location_display')
    status = serializers.CharField(source='get_status_display')

    class Meta:
        '''
        Meta class to define the Model to use for ModelSerializer
        '''
        model = Emergency
        fields = (
            'user',
            'reason',
            'location',
            'status'
        )


class TransactionSerializer(serializers.ModelSerializer):
    '''
    Serializer to serialize Transaction objects
    '''
    class Meta:
        '''
        Meta class to define the Model to use for ModelSerializer
        '''
        model = Transaction
        fields = (
            'id',
            'prescription',
            'units'
        )


class InventorySerializer(serializers.ModelSerializer):
    '''
    Serializer to serialize Inventory objects
    '''
    category = serializers.CharField(source='get_category_display')
    class Meta:
        '''
        Meta class to define the Model to use for ModelSerializer
        '''
        model = Inventory
        fields = (
            'id',
            'name',
            'units',
            'category',
            'cost_per_unit'
        )

class DocumentSerializer(serializers.ModelSerializer):
    '''
    Serializer to serialize Document objects
    '''
    filename = serializers.CharField(source='file.name', read_only=True)
    filesize = serializers.CharField(source='file.size', read_only=True)
    class Meta:
        '''
        Meta class to define the Model to use for ModelSerializer
        '''
        model = Document
        fields = (
            'id',
            'filename',
            'filesize',
        )
