from django import forms
from .models import Patient
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()

class PatientUserForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    phone = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone', 'password1', 'password2']

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = [
            'date_of_birth', 'gender', 'blood_group', 'height', 'weight',
            'allergies', 'medical_history', 'emergency_contact',
            'emergency_phone', 'insurance_provider', 'insurance_number',
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'allergies': forms.Textarea(attrs={'rows': 3}),
            'medical_history': forms.Textarea(attrs={'rows': 3}),
        }