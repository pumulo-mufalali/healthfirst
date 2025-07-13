from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from .decorators import unauthorized_user
from .forms import UserRegistrationForm
from patients.models import Patient
from appointments.models import Appointment, MedicalRecord
from datetime import date as today_date


def home(request):
    return render(request, 'accounts/home.html')


def dashboard(request):
    today = today_date.today()
    
    appointments = Appointment.objects.all()
    todays_appointment = appointments.filter(date=today).count
    total_appointment = appointments.count()

    total_patients = Patient.objects.count()

    total_record = MedicalRecord.objects.all().count()

    context = {
        'appointments':appointments,
        'total_appointment':total_appointment,
        'todays_appointment':todays_appointment,

        'total_medical_record':total_record,
        'total_patients':total_patients,
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