from django.contrib.auth import get_user_model

User = get_user_model()

def user_type(request):
    return {
        'is_patient': hasattr(request.user, 'patient_profile'),
        'is_doctor': hasattr(request.user, 'doctor_profile'),
    }