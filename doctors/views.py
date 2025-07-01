from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Doctor
from django.contrib.auth import get_user_model
from .form import DoctorForm, DoctorUserForm

User = get_user_model()

def is_admin_or_staff(user):
    return user.is_authenticated and (user.user_type in ['admin', 'staff'] or user.is_superuser)

# @login_required
def doctor_list(request):
    doctors = Doctor.objects.select_related('user').all()
    return render(request, 'doctors/list.html', {
        'doctors': doctors,
    })

# @login_required
def doctor_detail(request, pk):
    doctor = get_object_or_404(
        Doctor.objects.select_related('user').prefetch_related('availabilities'),
        user_id=pk
    )
    return render(request, 'doctors/detail.html', {'doctor': doctor})

# @login_required
# @user_passes_test(is_admin_or_staff)
def doctor_create(request):
    if request.method == 'POST':
        user_form = DoctorUserForm(request.POST)
        doctor_form = DoctorForm(request.POST)
        if user_form.is_valid() and doctor_form.is_valid():
            user = user_form.save(commit=False)
            user.user_type = 'doctor'
            user.save()

            doctor = doctor_form.save(commit=False)
            doctor.user = user
            doctor.save()

            return redirect('doctors:doctor_detail', pk=doctor.user_id)
    else:
        user_form = DoctorUserForm()
        doctor_form = DoctorForm()

    context = {'user_form': user_form, 'form': doctor_form, 'title': 'Create Doctor'}

    
    return render(request, 'doctors/form.html', context)

# @login_required
def doctor_update(request, pk):
    doctor = get_object_or_404(Doctor, user_id=pk)
    if not (request.user == doctor.user or is_admin_or_staff(request.user)):
        return redirect('home')
        
    if request.method == 'POST':
        form = DoctorForm(request.POST, instance=doctor)
        if form.is_valid():
            form.save()
            print('YA BITCHHHHHHH')
            return redirect('doctors:doctor_detail', pk)
    else:
        form = DoctorForm(instance=doctor)

    context = {'form': form, 'title': 'Update Doctor Profile',}

    return render(request, 'doctors/form.html', context)