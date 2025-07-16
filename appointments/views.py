from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Appointment, MedicalRecord, Prescription
from .forms import AppointmentForm, PrescriptionForm, MedicalRecordForm, AppointmentStatusForm
from django.utils import timezone
from datetime import date as today_date
from doctors.models import Doctor


import stripe
from django.conf import settings
from django.views import View
from django.http import JsonResponse

stripe.api_key = settings.STRIPE_SECRET_KEY


def appointment_list(request):
    today = today_date.today()

    todays_appointment = Appointment.objects.filter(date=today)

    if hasattr(request.user, 'patient_profile'):
        appointments = Appointment.objects.filter(
            patient=request.user.patient_profile
        ).order_by('date', 'start_time')
    elif hasattr(request.user, 'doctor_profile'):
        appointments = Appointment.objects.filter(
            doctor=request.user.doctor_profile
        ).order_by('date', 'start_time')
    else:
        appointments = Appointment.objects.all().order_by('date', 'start_time')
    
    context = {
        'today': todays_appointment,
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
    
    # Check permission - only doctors and staff can add prescriptions
    if not (request.user.is_staff or hasattr(request.user, 'doctor_profile')):
        messages.error(request, "Only authorized medical staff can add prescriptions")
        return redirect('appointments:detail', pk=appointment_pk)
    
    if request.method == 'POST':
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            prescription = form.save(commit=False)
            prescription.appointment = appointment
            prescription.prescribed_by = request.user.doctor_profile if hasattr(request.user, 'doctor_profile') else None
            prescription.save()
            messages.success(request, 'Prescription added successfully')
            return redirect('appointments:detail', pk=appointment_pk)
    else:
        form = PrescriptionForm(initial={
            'prescribed_date': timezone.now().date()
        })
    
    context = {
        'form': form,
        'appointment': appointment,
        'title': 'Add New Prescription'
    }
    return render(request, 'appointments/prescription_form.html', context)


def add_medical_record(request, appointment_pk):
    appointment = get_object_or_404(Appointment, pk=appointment_pk)
    
    if not (request.user.is_staff or hasattr(request.user, 'doctor_profile')):
        messages.error(request, "Only authorized medical staff can add medical records")
        return redirect('appointments:detail', pk=appointment_pk)

    if request.method == 'POST':
        form = MedicalRecordForm(request.POST)
        if form.is_valid():
            medical_record = form.save(commit=False)
            medical_record.appointment = appointment
            medical_record.created_by = request.user.doctor_profile if hasattr(request.user, 'doctor_profile') else None
            medical_record.save()

            messages.success(request, 'Medical record added successfully')
            return redirect('appointments:detail', pk=appointment_pk)
    else:
        form = MedicalRecordForm(initial={
            'created_at': timezone.now()
        })

    context = {
        'form': form,
        'appointment': appointment,
        'title': 'Add Medical Record',
    }
    return render(request, 'appointments/medical_record_form.html', context)


def medical_record_list(request, pk):

    doctor = Doctor.objects.get(user_id=pk)

    appointments = Appointment.objects.filter(doctor_id=doctor.id)
    context = {
        'appointments': appointments,
    }
    return render(request, 'appointments/record_list.html', context)


def doctor_prescriptions(request):
    if not hasattr(request.user, 'doctor_profile'):
        return render(request, '403.html', status=403)

    doctor = request.user.doctor_profile

    prescriptions = Prescription.objects.select_related(
        'appointment__patient__user'
    ).filter(
        appointment__doctor=doctor
    ).order_by('-prescribed_date')

    context = {
        'prescriptions': prescriptions
    }
    return render(request, 'appointments/prescriptions.html', context)

# STRIPPPPPPPPPPPPPPPPPPPPPPPPPPPEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE

class CreateCheckoutSessionView(View):
    def post(self, request, appointment_id, *args, **kwargs):
        # YOUR_DOMAIN = 'http://localhost:8000'
        YOUR_DOMAIN = request.build_absolute_uri('/')[:-1]

        appointment = get_object_or_404(Appointment, id=appointment_id)

        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        'price': 'price_12345',  # Replace with your actual Stripe Price ID
                        'quantity': 1,
                    },
                ],
                mode='payment',
                metadata={
                    'appointment_id': appointment.id,
                    'patient_id': appointment.patient.id,
                    'doctor_id': appointment.doctor.id
                },
                success_url=YOUR_DOMAIN + '/appointments/payment-success/',
                cancel_url=YOUR_DOMAIN + '/appointments/payment-cancel/',
            )
            return redirect(checkout_session.url, code=303)
        except Exception as e:
            return JsonResponse({'error': str(e)})
        

def payment_success(request):
    return render(request, 'appointments/payment_success.html')

def payment_cancel(request):
    return render(request, 'appointments/payment_cancel.html')