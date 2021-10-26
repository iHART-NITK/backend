from django.db import models
from django.contrib.auth.models import AbstractUser

# User Model, stores information on all personnel


class User(AbstractUser):
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

    # TODO: Create default image and set this to default value
    photo = models.ForeignKey(
        'Document',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="User Photo ID")
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

# Medical History Model, stores data on each user's medical history


class MedicalHistory(models.Model):
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

# Specialization table can be dropped, instead get_FOO_display can be used from User table itself
# https://docs.djangoproject.com/en/3.2/ref/models/instances/#django.db.models.Model.get_FOO_display

# Schedule Model, stores data on each doctor's schedule


class Schedule(models.Model):
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

# Appointment Model, stores data on all scheduled appointments


class Appointment(models.Model):
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

# Diagnosis Model, stores data on the diagnosis given for a particular visit


class Diagnosis(models.Model):
    appointment = models.ForeignKey(
        'Appointment',
        on_delete=models.CASCADE,
        verbose_name="Appointment ID")
    diagnosis = models.TextField(verbose_name="Diagnosis")

# Prescription Model, stores data on the prescriptions that are related to
# a particular diagnosis


class Prescription(models.Model):
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

# Transaction Model, stores data on distribution of inventory to students
# & faculty


class Transaction(models.Model):
    prescription = models.ForeignKey(
        'Prescription',
        on_delete=models.CASCADE,
        verbose_name="Prescription ID")
    units = models.PositiveIntegerField(verbose_name="Units")

# Inventory Model, stores data on the inventory of the HCC


class Inventory(models.Model):
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

# Emergency Model, stores data on Emergency requests made


class Emergency(models.Model):
    # TODO: Add more locations or enable geolocation access
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

# Document Model, stores all documents and files in the database


class Document(models.Model):
    file = models.BinaryField()

# Medical Certificate Model, stores data on the sickness certificates to
# be submitted by students


class MedicalCertificate(models.Model):
    diagnosis = models.ForeignKey(
        'Diagnosis',
        on_delete=models.CASCADE,
        verbose_name="Diagnosis ID")
    document = models.ForeignKey(
        'Document',
        on_delete=models.CASCADE,
        verbose_name="Document ID")

# Config Model, stores basic config values


class Config(models.Model):
    obj = models.JSONField()
