from django.db import models
from django.contrib.auth import get_user_model
from patients.models import Patient
from doctors.models import Doctor
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
# from djstripe.models import PaymentIntent

User = get_user_model()

class Appointment(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    
    APPOINTMENT_TYPE_CHOICES = (
        ('in_person', 'In-Person'),
        ('telemedicine', 'Telemedicine'),
    )

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    date = models.DateField()
    time = models.TimeField(timezone.now)
    start_time = models.TimeField()
    end_time = models.TimeField()
    reason = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    appointment_type = models.CharField(max_length=20, choices=APPOINTMENT_TYPE_CHOICES, default='in_person')
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['date', 'start_time']
        unique_together = ('doctor', 'date', 'start_time')

    def __str__(self):
        return f"{self.patient.user.get_full_name()} with Dr. {self.doctor.user.last_name} on {self.date} at {self.start_time}"

class Prescription(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='prescriptions')
    medication = models.CharField(max_length=100)
    dosage = models.CharField(max_length=50)
    instructions = models.TextField()
    prescribed_date = models.DateField(default=timezone.now)
    refills = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.medication} for {self.appointment.patient.user.get_full_name()}"

class MedicalRecord(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='medical_records')
    diagnosis = models.TextField()
    treatment = models.TextField()
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Record for {self.appointment.patient.user.get_full_name()} on {self.created_at.date()}"
    
# class Payment(models.Model):
#     appointment = models.ForeignKey('Appointment', on_delete=models.CASCADE)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     stripe_payment_intent = models.ForeignKey(PaymentIntent, on_delete=models.SET_NULL, null=True)
#     status = models.CharField(max_length=20, choices=[
#         ('pending', 'Pending'),
#         ('completed', 'Completed'),
#         ('failed', 'Failed'),
#         ('refunded', 'Refunded'),
#     ], default='pending')
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"Payment #{self.id} - {self.status}"