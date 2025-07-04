from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from .decorators import admin_only, unauthorized_user, allowed_user
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegistrationForm, UserProfileForm
from patients.models import Patient
from appointments.models import Appointment
from datetime import date


def home(request):
    return render(request, 'accounts/home.html')


# @allowed_user('staff')
# @admin_only
def dashboard(request):
    todays_date = date.today
    
    appointment = Appointment.objects.all()
    
    todays_appointments = Appointment.objects.filter(date=todays_date)
    total_appointment = appointment.count()

    total_patients = Patient.objects.all().count()
    context = {
        'total_patients':total_patients,
        'total_appointment':total_appointment,
        'todays_appointments':todays_appointments,
    }
    return render(request, 'accounts/dashboard.html', context)

@unauthorized_user
def loginPage(request):
  if request.method == 'POST':
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)
    
    if user is not None:
        # login(request, user)
        
        if user.user_type == 'patient':
            return redirect('patients:patient_list')
        elif user.user_type == 'doctor':
            return redirect('doctors:doctor_list')
        else:
            return redirect('home')
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
                return redirect('patients:patient_list')

            elif user.user_type == 'doctor':
                return redirect('doctors:doctor_list')
            else:
                return redirect('home')
    else:
        form = UserRegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})



# def user_login(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(request, data=request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             login(request, user)
#             return redirect('dashboard')
#     else:
#         form = AuthenticationForm()
#     return render(request, 'accounts/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')

# @login_required
# def profile(request):
#     if request.method == 'POST':
#         form = UserProfileForm(request.POST, request.FILES, instance=request.user)
#         if form.is_valid():
#             form.save()
#             return redirect('profile')
#     else:
#         form = UserProfileForm(instance=request.user)
#     return render(request, 'accounts/profile.html', {'form': form})