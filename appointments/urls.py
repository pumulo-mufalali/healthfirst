from django.urls import path
from . import views

app_name = 'appointments'

urlpatterns = [
    path('', views.appointment_list, name='list'),
    path('create/', views.appointment_create, name='create'),
    path('<int:pk>/', views.appointment_detail, name='detail'),
    path('<int:appointment_pk>/prescription/', views.add_prescription, name='add_prescription'),
    path('<int:appointment_pk>/add_medical_record/', views.add_medical_record, name='add_medical_record'),

    path('medical_record_list/<int:pk>/', views.medical_record_list, name='record_list'),
    # path('record_list/<int:pk>/', views.add_medical_record, name='add_medical_record'),

    # path('create-payment/<int:appointment_id>/', views.create_payment, name='create_payment'),
    # path('stripe-webhook/', views.stripe_webhook, name='stripe_webhook'),
]