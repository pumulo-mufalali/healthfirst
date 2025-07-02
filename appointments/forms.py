from django import forms
from .models import Appointment, Prescription, MedicalRecord
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import date

User = get_user_model()

class AppointmentForm(forms.ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'min': date.today()}),
        initial=date.today()
    )
    start_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    end_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))

    class Meta:
        model = Appointment
        fields = ['doctor', 'date', 'start_time', 'end_time', 'reason', 'appointment_type']
        widgets = {
            'reason': forms.Textarea(attrs={'rows': 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        
        if start_time and end_time and start_time >= end_time:
            raise forms.ValidationError("End time must be after start time")
        
        return cleaned_data

class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['medication', 'dosage', 'instructions', 'refills', 'is_active']
        widgets = {
            'instructions': forms.Textarea(attrs={'rows': 3}),
        }

class MedicalRecordForm(forms.ModelForm):
    class Meta:
        model = MedicalRecord
        fields = ['diagnosis', 'treatment', 'notes']
        widgets = {
            'diagnosis': forms.Textarea(attrs={'rows': 3}),
            'treatment': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 2}),
        }

class AppointmentStatusForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['status', 'notes']