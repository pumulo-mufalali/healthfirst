from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
  path('get-doctor-fee/', views.get_doctor_fee, name='get_doctor_fee'),
  path('pay/<int:appointment_id>/', views.create_checkout_session, name='create_checkout_session'),
]