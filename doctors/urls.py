from django.urls import path
from . import views

app_name = 'doctors'

urlpatterns = [
    path('', views.doctor_list, name='list'),
    path('create/', views.doctor_create, name='doctor_create'),
    path('<int:pk>/', views.doctor_detail, name='doctor_detail'),
    path('<int:pk>/update/', views.doctor_update, name='doctor_update'),
    
    # # Specialization URLs
    # path('specializations/', views.specialization_list, name='specialization_list'),
    # path('specializations/create/', views.specialization_create, name='specialization_create'),
]