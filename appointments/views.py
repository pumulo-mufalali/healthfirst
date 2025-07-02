from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Appointment, Prescription, MedicalRecord
from .forms import AppointmentForm, PrescriptionForm, MedicalRecordForm, AppointmentStatusForm
from patients.models import Patient
from doctors.models import Doctor
from django.utils import timezone
from datetime import date


def appointment_list(request):
    today = date.today()
    if hasattr(request.user, 'patient_profile'):
        appointments = Appointment.objects.filter(
            patient=request.user.patient_profile
        ).order_by('date', 'start_time')
    elif hasattr(request.user, 'doctor_profile'):
        appointments = Appointment.objects.filter(
            doctor=request.user.doctor_profile
        ).order_by('date', 'start_time')
    else:  # admin/staff
        appointments = Appointment.objects.all().order_by('date', 'start_time')
    
    context = {
        'today': today,
        'upcoming': appointments.filter(date__gte=today),
        'past': appointments.filter(date__lt=today),
    }
    return render(request, 'appointments/list.html', context)


def appointment_detail(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    
    # Check permission
    if not (request.user.is_staff or 
            hasattr(request.user, 'doctor_profile') and appointment.doctor == request.user.doctor_profile or
            hasattr(request.user, 'patient_profile') and appointment.patient == request.user.patient_profile):
        messages.error(request, "You don't have permission to view this appointment")
        return redirect('appointments:list')
    
    prescriptions = appointment.prescriptions.all()
    medical_records = appointment.medical_records.all()
    
    if request.method == 'POST':
        form = AppointmentStatusForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Appointment status updated')
            return redirect('appointments:detail', pk=pk)
    else:
        form = AppointmentStatusForm(instance=appointment)
    
    context = {
        'appointment': appointment,
        'prescriptions': prescriptions,
        'medical_records': medical_records,
        'form': form,
    }
    return render(request, 'appointments/detail.html', context)


def appointment_create(request):
    if not hasattr(request.user, 'patient_profile'):
        messages.error(request, "Only patients can book appointments")
        return redirect('appointments:list')
    
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user.patient_profile
            appointment.save()
            messages.success(request, 'Appointment booked successfully')
            return redirect('appointments:detail', pk=appointment.pk)
    else:
        form = AppointmentForm()
    
    context = {'form': form}
    return render(request, 'appointments/form.html', context)


def add_prescription(request, appointment_pk):
    appointment = get_object_or_404(Appointment, pk=appointment_pk)
    
    if not (request.user.is_staff or hasattr(request.user, 'doctor_profile')):
        messages.error(request, "Only doctors can add prescriptions")
        return redirect('appointments:detail', pk=appointment_pk)
    
    if request.method == 'POST':
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            prescription = form.save(commit=False)
            prescription.appointment = appointment
            prescription.save()
            messages.success(request, 'Prescription added successfully')
            return redirect('appointments:detail', pk=appointment_pk)
    else:
        form = PrescriptionForm()
    
    context = {
        'form': form,
        'appointment': appointment,
        'title': 'Add Prescription'
    }
    return render(request, 'appointments/prescription_form.html', context)


def add_medical_record(request, appointment_pk):
    appointment = get_object_or_404(Appointment, pk=appointment_pk)
    
    if not (request.user.is_staff or hasattr(request.user, 'doctor_profile')):
        messages.error(request, "Only doctors can add medical records")
        return redirect('appointments:detail', pk=appointment_pk)
    
    if request.method == 'POST':
        form = MedicalRecordForm(request.POST)
        if form.is_valid():
            medical_record = form.save(commit=False)
            medical_record.appointment = appointment
            medical_record.save()
            messages.success(request, 'Medical record added successfully')
            return redirect('appointments:detail', pk=appointment_pk)
    else:
        form = MedicalRecordForm()
    
    context = {
        'form': form,
        'appointment': appointment,
        'title': 'Add Medical Record'
    }
    return render(request, 'appointments/medical_record_form.html', context)