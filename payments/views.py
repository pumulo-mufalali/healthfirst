import stripe
from django.conf import settings
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from doctors.models import Doctor
from appointments.models import Appointment


stripe.api_key = settings.STRIPE_SECRET_KEY

def create_checkout_session(request, appointment_id):
    try:
        # Get the appointment object
        from appointments.models import Appointment  # Adjust import based on your app structure
        
        appointment = Appointment.objects.get(id=appointment_id)
        doctor = appointment.doctor
        consultation_fee = doctor.consultation_fee
        
        # Convert to cents for Stripe (Stripe expects amounts in smallest currency unit)
        amount_in_cents = int(consultation_fee * 100)
        
        # Create a dynamic price instead of using a fixed price ID
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'ZMW',  # Zambian Kwacha
                    'product_data': {
                        'name': f'Consultation with Dr. {doctor.user.get_full_name()}',
                        'description': f'Medical consultation appointment on {appointment.date} at {appointment.time}',
                    },
                    'unit_amount': amount_in_cents,
                },
                'quantity': 1,
            }],
            mode='payment',  # Changed from 'subscription' to 'payment' for one-time payments
            success_url=request.build_absolute_uri(
                f'/appointments/payment-success/?session_id={{CHECKOUT_SESSION_ID}}'
            ),
            cancel_url=request.build_absolute_uri(
                f'/appointments/{appointment_id}/payment-cancel/'
            ),
            metadata={
                'appointment_id': appointment_id,
                'doctor_id': str(doctor.id),
                'consultation_fee': str(consultation_fee)
            },
            customer_email=request.user.email,  # Pre-fill customer email
        )
        return redirect(checkout_session.url)
        
    except Appointment.DoesNotExist:
        return JsonResponse({'error': 'Appointment not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt  # Temporarily disable CSRF for testing
def get_doctor_fee(request):
    doctor_id = request.GET.get('doctor_id')
    
    if not doctor_id:
        return JsonResponse({'error': 'No doctor ID provided'}, status=400)
    
    try:
        # Import your Doctor model - adjust this import to match your app structure
        from doctors.models import Doctor  # or your actual import path
        
        doctor = Doctor.objects.get(id=doctor_id)
        fee = float(doctor.consultation_fee) if doctor.consultation_fee else 0.0
        
        return JsonResponse({
            'fee': fee,
            'doctor_name': f"{doctor.user.get_full_name()}"
        })
        
    except Doctor.DoesNotExist:
        return JsonResponse({'error': 'Doctor not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def payment_success(request):
    return render(request, 'payments/payment_success.html')

def payment_cancel(request):
    return render(request, 'payments/payment_cancel.html')