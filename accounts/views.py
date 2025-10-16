from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from .decorators import unauthorized_user
from .forms import UserRegistrationForm
from patients.models import Patient
from appointments.models import Appointment, MedicalRecord
from datetime import date as today_date
from .utils import DashboardCalculator, TemplateDataProcessor, NotificationProcessor

from doctors.models import Doctor


def home(request):
    return render(request, 'accounts/home.html')


def dashboard(request):
    dashboard_stats = DashboardCalculator.get_dashboard_stats(request.user.user_type)
    
    # Get notifications
    notifications = NotificationProcessor.get_system_notifications(request.user)
    
    # Format data for templates
    if 'recent_appointments' in dashboard_stats:
        dashboard_stats['formatted_recent_appointments'] = TemplateDataProcessor.format_appointment_data(
            dashboard_stats['recent_appointments']
        )
    
    context = {
        **dashboard_stats,
        'notifications': notifications,
    }
    return render(request, 'accounts/dashboard.html', context)


def userLogout(request):
    logout(request)
    return redirect('accounts:login')


@unauthorized_user
def loginPage(request):
  if request.method == 'POST':
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)
    
    if user is not None:
        login(request, user)
        
        if user.user_type == 'patient':
            return redirect('patients:patient_dashboard')
        elif user.user_type == 'doctor':
            return redirect('doctors:doctor_dashboard')
        else:
            return redirect('accounts:dashboard')
    else:
        return render(request, 'accounts/login.html', {'error': 'Invalid credentials'})
  
  return render(request, 'accounts/login.html')

@unauthorized_user
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful.')

            if user.user_type == 'patient':
                return redirect('patients:patient_dashboard')

            elif user.user_type == 'doctor':
                return redirect('doctors:doctor_dashboard')
            else:
                return redirect('home')
    else:
        form = UserRegistrationForm()

    return render(request, 'accounts/register.html', {'form':form})


@unauthorized_user
def doctor_register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful.')

            return redirect('doctors:doctor_dashboard')
    else:
        form = UserRegistrationForm()

    return render(request, 'accounts/doctor_register.html', {'form':form})

def services(request):
    return render(request, 'accounts/services.html')

def doctor_list(request):
    doctors = Doctor.objects.all()

    return render(request, 'accounts/doctor_list.html', {'doctors':doctors})