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