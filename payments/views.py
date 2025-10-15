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
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price': settings.STRIPE_CONSULTATION_PRICE_ID,
                'quantity': 1,
            }],
            mode='subscription',
            success_url=request.build_absolute_uri('/appointments/payment-success/'),
            cancel_url=request.build_absolute_uri('/appointments/payment-cancel/'),
            metadata={'appointment_id': appointment_id}
        )
        return redirect(checkout_session.url)
    except Exception as e:
        return JsonResponse({'error': str(e)})


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