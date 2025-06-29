from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Patient
from .forms import PatientForm, PatientUserForm
from django.contrib.auth import get_user_model

User = get_user_model()

def is_admin_or_staff(user):
    return user.is_authenticated and (user.user_type in ['admin', 'staff'] or user.is_superuser)


# @user_passes_test(is_admin_or_staff)
def patient_list(request):
    patients = Patient.objects.all()
    return render(request, 'patients/list.html', {'patients': patients})


def patient_detail(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if not (request.user == patient.user or is_admin_or_staff(request.user)):
        return redirect('home')  # Or permission denied
    return render(request, 'patients/detail.html', {'patient': patient})


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
            return redirect('patients:detail', pk=patient.pk)
    else:
        user_form = PatientUserForm()
        patient_form = PatientForm()
    return render(request, 'patients/form.html', {
        'user_form': user_form,
        'form': patient_form,
        'title': 'Create Patient'
    })

def patient_update(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if not (request.user == patient.user or is_admin_or_staff(request.user)):
        return redirect('home')  # Or permission denied
        
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            return redirect('patients:detail', pk=patient.pk)
    else:
        form = PatientForm(instance=patient)
    return render(request, 'patients/form.html', {
        'form': form,
        'title': 'Update Patient'
    })