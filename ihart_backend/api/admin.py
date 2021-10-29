from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin

admin.site.register(User, UserAdmin)
admin.site.register(MedicalHistory)
admin.site.register(Schedule)
admin.site.register(Appointment)
admin.site.register(Diagnosis)
admin.site.register(Prescription)
admin.site.register(Transaction)
admin.site.register(Inventory)
admin.site.register(Emergency)
admin.site.register(Document)
admin.site.register(MedicalCertificate)
admin.site.register(Config)
