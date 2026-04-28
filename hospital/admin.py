from django.contrib import admin

from hospital.models import Patient, Appointment, Doctor

# Register your models here.
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Appointment)