'''
Models (Database Schema) for each entity is stored here.
The Django ORM uses this schema to create tables in the database
and perform CRUD operations on the database.
'''
from django.db import models
from django.contrib.auth.models import AbstractUser
from gdstorage.storage import GoogleDriveStorage

# Define Google Drive Storage
gd_storage = GoogleDriveStorage()

class User(AbstractUser):
    '''
    User Model, stores information on all personnel
    '''
    USER_TYPE_CHOICES = [
        ('Stu', "Student"),
        ('Fac', "Faculty"),
        ('Sta', "HCC Staff"),
        ('Pae', "Paediatrician"),
        ('Den', "Dentist"),
        ('Ort', "Orthopedic Surgeon"),
        ('Der', "Dermatologist"),
        ('Psy', "Psychiatrist"),
        ('Oph', "Ophthalmologist"),
        ('Gen', "General Medicine"),
        ('Psc', "Psychological Counselor"),
        ('Eye', "Eye Specialist"),
        ('Ent', "ENT Surgeon"),
        ('Gyn', "Gynaecologist"),
        ('Ayu', "Ayurvedic Consultant"),
        ('Hos', "Hospital")
    ]

    GENDER_CHOICES = [
        ('M', "Male"),
        ('F', "Female"),
        ('O', "Other"),
        ('N', "Would not like to disclose")
    ]

    photo = models.URLField(
        verbose_name="Profile Image URL",
        default="https://www.gravatar.com/avatar/?d=mp",
        max_length=256)
    user_type = models.CharField(
        max_length=3,
        choices=USER_TYPE_CHOICES,
        default='Stu',
        verbose_name="User Type")
    middle_name = models.CharField(
        max_length=30,
        verbose_name="Middle Name",
        blank=True)
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        verbose_name="Gender")
    phone = models.CharField(max_length=20, verbose_name="User Contact Number")
    emergency_phone = models.CharField(
        max_length=20, verbose_name="Emergency Contact Number")
    forgot_pwd_token = models.CharField(
        max_length=50, verbose_name="Forgot Password Token")
    customer_id = models.CharField(max_length=30, verbose_name="Google Customer ID")

class MedicalHistory(models.Model):
    '''
    Medical History Model, stores data on each user's medical history
    '''
    CATEGORY_CHOICES = [
        ('A', "Allergies"),
        ('M', "Medications"),
        ('S', "Surgery")
    ]

    user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        verbose_name="User ID")
    category = models.CharField(
        max_length=1,
        choices=CATEGORY_CHOICES,
        verbose_name="Category")
    description = models.TextField(verbose_name="Description")

class Schedule(models.Model):
    '''
    Schedule Model, stores data on each doctor's schedule
    '''
    DAY_CHOICES = [
        ('Mon', "Monday"),
        ('Tue', "Tuesday"),
        ('Wed', "Wednesday"),
        ('Thu', "Thursday"),
        ('Fri', "Friday"),
        ('Sat', "Saturday"),
        ('Sun', "Sunday")
    ]

    user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        verbose_name="User ID")
    entry_time = models.TimeField(verbose_name="Doctor Entry Time")
    exit_time = models.TimeField(verbose_name="Doctor Exit Time")
    day = models.CharField(
        max_length=3,
        choices=DAY_CHOICES,
        verbose_name="Day of Visit")

class Appointment(models.Model):
    '''
    Appointment Model, stores data on all scheduled appointments
    '''
    STATUS_CHOICES = [
        ('VI', "Visited"),
        ('DM', "Doctor Missing"),
        ('PM', "Patient Missing"),
        ('EX', "Expired"),
        ('CA', "Cancelled")
    ]

    schedule = models.ForeignKey(
        'Schedule',
        on_delete=models.CASCADE,
        verbose_name="Schedule ID")
    user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        verbose_name="User ID")
    date = models.DateField(verbose_name="Appointment Date")
    start_time = models.TimeField(verbose_name="Start Time")
    status = models.CharField(
        max_length=2,
        choices=STATUS_CHOICES,
        verbose_name="Status")
    create_time = models.TimeField(
        auto_now_add=True,
        verbose_name="Create Time")

class Diagnosis(models.Model):
    '''
    Diagnosis Model, stores data on the diagnosis given for a particular visit
    '''
    appointment = models.ForeignKey(
        'Appointment',
        on_delete=models.CASCADE,
        verbose_name="Appointment ID")
    diagnosis = models.TextField(verbose_name="Diagnosis")




class Prescription(models.Model):
    '''
    Prescription Model, stores data on the prescriptions that are related to a particular diagnosis
    '''

    diagnosis = models.ForeignKey(
        'Diagnosis',
        on_delete=models.CASCADE,
        verbose_name="Diagnosis ID")
    inventory = models.ForeignKey(
        'Inventory',
        on_delete=models.CASCADE,
        verbose_name="Inventory ID")
    dosage = models.CharField(max_length=10, verbose_name="Daily Dosage")
    medicine_units = models.PositiveIntegerField(verbose_name="Medicine Units")

class Transaction(models.Model):
    '''
    Transaction Model, stores data on distribution of inventory to students & faculty
    '''
    prescription = models.ForeignKey(
        'Prescription',
        on_delete=models.CASCADE,
        verbose_name="Prescription ID")
    units = models.PositiveIntegerField(verbose_name="Units")

class Inventory(models.Model):
    '''
    Inventory Model, stores data on the inventory of the HCC
    '''
    CATEGORY_CHOICES = [
        ('M', "Medicine"),
        ('E', "Equipment")
    ]

    name = models.CharField(
        max_length=60,
        unique=True,
        verbose_name="Item Name")
    units = models.PositiveIntegerField(default=0, verbose_name="Units")
    category = models.CharField(
        max_length=1,
        choices=CATEGORY_CHOICES,
        verbose_name="Category")
    cost_per_unit = models.FloatField(verbose_name="Cost Per Unit")

class Emergency(models.Model):
    '''
    Emergency Model, stores data on Emergency requests made
    '''
    # To do: Add more locations or enable geolocation access
    LOCATION_CHOICES = [
        ('BEA', "Beach Gate"),
        ('UND', "Underpass"),
        ('LHC', "Lecture Hall Complex - C"),
        ('GIH', "Girls Hostels"),
        ('MEC', "Mechanical Department"),
        ('BBC', "Basketball Court & Swimming Pool"),
        ('SJA', "Silver Jubilee Auditorium"),
        ('SBI', "SBI Bank"),
        ('MET', "Mega Towers"),
        ('BOH', "Boys Hostels"),
        ('PAV', "Pavillion"),
        ('SAC', "Student Activity Center"),
        ('MAB', "Main Building")
    ]

    STATUS_CHOICES = [
        ('R', "Received"),
        ('A', "Acknowledged")
    ]

    user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        verbose_name="User ID")
    reason = models.TextField(verbose_name="Reason for Emergency")
    location = models.CharField(
        max_length=3,
        choices=LOCATION_CHOICES,
        verbose_name="Location")
    status = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES,
        verbose_name="Status")

class Document(models.Model):
    '''
    Document Model, stores all documents and files in the database
    '''
    file = models.FileField(storage=gd_storage)

class MedicalCertificate(models.Model):
    '''
    Medical Certificate Model, stores data on the sickness certificates to be submitted by students
    '''
    diagnosis = models.ForeignKey(
        'Diagnosis',
        on_delete=models.CASCADE,
        verbose_name="Diagnosis ID")
    document = models.ForeignKey(
        'Document',
        on_delete=models.CASCADE,
        verbose_name="Document ID")

class Config(models.Model):
    '''
    Config Model, stores basic config values
    '''
    obj = models.JSONField()
