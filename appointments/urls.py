from django.urls import path
from . import views

app_name = 'appointments'

urlpatterns = [
    path('', views.appointment_list, name='list'),
    path('create/', views.appointment_create, name='create'),
    path('<int:pk>/', views.appointment_detail, name='detail'),
    path('<int:appointment_pk>/prescription/', views.add_prescription, name='add_prescription'),
    path('<int:appointment_pk>/record/', views.add_medical_record, name='add_medical_record'),
]