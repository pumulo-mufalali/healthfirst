from django.contrib import admin
from .models import Appointment, Prescription, MedicalRecord

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'date', 'start_time', 'status', 'appointment_type')
    list_filter = ('status', 'appointment_type', 'date')
    search_fields = ('patient__user__first_name', 'patient__user__last_name', 
                    'doctor__user__first_name', 'doctor__user__last_name')
    date_hierarchy = 'date'
    ordering = ('-date', '-start_time')

@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('appointment', 'medication', 'dosage', 'prescribed_date', 'is_active')
    list_filter = ('is_active', 'prescribed_date')
    search_fields = ('medication', 'appointment__patient__user__first_name')

@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ('appointment', 'created_at')
    search_fields = ('appointment__patient__user__first_name', 'diagnosis')
    date_hierarchy = 'created_at'