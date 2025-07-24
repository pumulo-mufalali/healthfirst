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
            mode='payment',
            success_url=request.build_absolute_uri('/appointments/payment-success/'),
            cancel_url=request.build_absolute_uri('/appointments/payment-cancel/'),
            metadata={'appointment_id': appointment_id}
        )
        return redirect(checkout_session.url)
    except Exception as e:
        return JsonResponse({'error': str(e)})

def get_doctor_fee(request):
    doctor_id = request.GET.get('doctor_id')
    try:
        doctor = Doctor.objects.get(id=doctor_id)
        return JsonResponse({'fee': float(doctor.consultation_fee)})
    except (Doctor.DoesNotExist, ValueError, TypeError):
        return JsonResponse({'fee': None})

def payment_success(request):
    return render(request, 'payments/payment_success.html')

def payment_cancel(request):
    return render(request, 'payments/payment_cancel.html')



# class CreateCheckoutSessionView(View):
#     def post(self, request, appointment_id, *args, **kwargs):
#         YOUR_DOMAIN = request.build_absolute_uri('/')[:-1]
#         stripe.api_key = settings.STRIPE_SECRET_KEY

#         appointment = get_object_or_404(Appointment, id=appointment_id)
#         try:
#             checkout_session = stripe.checkout.Session.create(
#                 line_items=[
#                     {
#                         'price': settings.STRIPE_CONSULTATION_PRICE_ID,
#                         'quantity': 1,
#                     },
#                 ],
#                 mode='payment',
#                 metadata={
#                     'appointment_id': appointment.id,
#                     'patient_id': appointment.patient.id,
#                     'doctor_id': appointment.doctor.id
#                 },
#                 success_url=YOUR_DOMAIN + '/appointments/payment-success/',
#                 cancel_url=YOUR_DOMAIN + '/appointments/payment-cancel/',
#             )
#             print('View createdddddddddddddddddddddddd')
#             return redirect(checkout_session.url, code=303)
#         except Exception as e:
#             return JsonResponse({'error': str(e)})


