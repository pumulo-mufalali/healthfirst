from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Patient
from .forms import PatientForm, PatientUserForm
from django.contrib.auth import get_user_model
from datetime import date
from appointments.models import Appointment

User = get_user_model()

def patient_dashboard(request):
    patient = get_object_or_404(Patient, user=request.user)
    today = date.today()
    
    # Get upcoming and past appointments
    appointments = Appointment.objects.filter(patient=patient).order_by('date', 'start_time')
    upcoming_appointments = appointments.filter(date__gte=today)[:3]
    past_appointments = appointments.filter(date__lt=today)[:3]
    
    # Calculate BMI if height and weight are available
    bmi = None
    if patient.weight and patient.height:
        try:
            # Convert height from feet'inches" to meters if needed
            if "'" in patient.height:
                feet, inches = patient.height.split("'")
                height_m = (float(feet) * 0.3048) + (float(inches.strip('"')) * 0.0254)
            else:
                height_m = float(patient.height) / 100  # assuming cm if no feet/inches
            
            bmi = round(float(patient.weight) / (height_m ** 2), 1)
        except:
            pass
    
    context = {
        'patient': patient,
        'upcoming_appointments': upcoming_appointments,
        'past_appointments': past_appointments,
        'bmi': bmi,
        'today': today,
    }
    return render(request, 'patients/dashboard.html', context)

def is_admin_or_staff(user):
    return user.is_authenticated and (user.user_type in ['admin', 'staff'] or user.is_superuser)


# @user_passes_test(is_admin_or_staff)
def patient_list(request):
    patients = Patient.objects.all()

    if hasattr(request.user, 'doctcor_profile'):
        doctors_patients = Appointment.objects.filter(doctor=request.user.doctor_profile).order_by('date', 'start_time')
        
    return render(request, 'patients/list.html', {'patients': patients})


def patient_detail(request, pk):
    patient = Patient.objects.get(user_id=pk)
    if not (request.user == patient.user or is_admin_or_staff(request.user)):
        return redirect('home')
    context = {'patient': patient}
    return render(request, 'patients/detail.html', context)


def patient_create(request):
    if request.method == 'POST':
        user_form = PatientUserForm(request.POST)
        patient_form = PatientForm(request.POST)
        if user_form.is_valid() and patient_form.is_valid():
            user = user_form.save(commit=False)
            user.user_type = 'patient'
            user.save()

            patient = patient_form.save(commit=False)
            patient.user = user
            patient.save()
            return redirect('patients:patient_detail', pk=patient.pk)
    else:
        user_form = PatientUserForm()
        patient_form = PatientForm()

    context = {'user_form': user_form, 'patient_form': patient_form, 'title': 'Create Patient'}

    return render(request, 'patients/form.html', context)

def patient_update(request, pk):
    patient = get_object_or_404(Patient, user_id=pk)
    patient_name = patient.user.first_name

    if not (request.user == patient.user or is_admin_or_staff(request.user)):
        return redirect('home')
        
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            return redirect('patients:patient_detail', pk=patient.user_id)
    else:
        form = PatientForm(instance=patient)

    context = {'patient_form': form, 'title': 'Update Patient', 'patient_name':patient_name}

    return render(request, 'patients/form.html', context)

def delete_patient(request, pk):
    patient = Patient.objects.get(user_id=pk)
    patient_name = patient.user.get_full_name()
    patient_deleted = None
    if request.method == 'POST':
        patient_deleted = patient.delete()
        return redirect('patients:patient_list')

    context = {
        'patient_deleted':patient_deleted,
        'patient_name':patient_name,
        'title':'Delete Patient'
    }

    return render(request, 'patients/delete_patient.html', context)
