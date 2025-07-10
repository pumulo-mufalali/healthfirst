from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Appointment
from .forms import AppointmentForm, PrescriptionForm, MedicalRecordForm, AppointmentStatusForm
from django.utils import timezone
from datetime import date as today_date

# import stripe
# from django.conf import settings
# from django.views.decorators.csrf import csrf_exempt
# from django.http import JsonResponse, HttpResponse
# from appointments.models import Appointment
# from .models import Payment

# stripe.api_key = settings.STRIPE_SECRET_KEY


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
    
    # Check permission - only doctors and staff can add medical records
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
        'title': 'Add Medical Record'
    }
    return render(request, 'appointments/medical_record_form.html', context)


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

# STRIPPPPPPPPPPPPPPPPPPPPPPPPPPPEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE
# def create_payment(request, appointment_id):
#     appointment = Appointment.objects.get(id=appointment_id)
    
#     try:
#         payment_intent = stripe.PaymentIntent.create(
#             amount=int(appointment.doctor.consultation_fee * 100),  # in cents
#             currency='usd',
#             metadata={
#                 'appointment_id': appointment.id,
#                 'patient_id': appointment.patient.id,
#                 'doctor_id': appointment.doctor.id
#             }
#         )
        
#         # Save payment record
#         payment = Payment.objects.create(
#             appointment=appointment,
#             amount=appointment.doctor.consultation_fee,
#             stripe_payment_intent_id=payment_intent.id,
#             status='pending'
#         )
        
#         return JsonResponse({
#             'clientSecret': payment_intent.client_secret
#         })
#     except Exception as e:
#         return JsonResponse({'error': str(e)}, status=400)

# @csrf_exempt
# def stripe_webhook(request):
#     payload = request.body
#     sig_header = request.META['HTTP_STRIPE_SIGNATURE']
#     event = None

#     try:
#         event = stripe.Webhook.construct_event(
#             payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
#         )
#     except ValueError as e:
#         return HttpResponse(status=400)
#     except stripe.error.SignatureVerificationError as e:
#         return HttpResponse(status=400)

#     # Handle payment success
#     if event['type'] == 'payment_intent.succeeded':
#         payment_intent = event['data']['object']
#         payment = Payment.objects.get(stripe_payment_intent_id=payment_intent['id'])
#         payment.status = 'completed'
#         payment.save()
        
#         # Update appointment status
#         appointment = payment.appointment
#         appointment.status = 'confirmed'
#         appointment.save()

#     return HttpResponse(status=200)