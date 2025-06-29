from django.shortcuts import render

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Appointment
from .forms import AppointmentForm
from datetime import date

@login_required
def appointment_list(request):
    today = date.today()
    upcoming = Appointment.objects.filter(date__gte=today).order_by('date', 'time')
    past = Appointment.objects.filter(date__lt=today).order_by('-date', '-time')
    return render(request, 'appointments/list.html', {
        'upcoming_appointments': upcoming,
        'past_appointments': past
    })

@login_required
def appointment_detail(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    return render(request, 'appointments/detail.html', {'appointment': appointment})

@login_required
def appointment_create(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.created_by = request.user
            appointment.save()
            return redirect('appointments:detail', pk=appointment.pk)
    else:
        form = AppointmentForm()
    return render(request, 'appointments/form.html', {'form': form})

@login_required
def appointment_update(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            return redirect('appointments:detail', pk=appointment.pk)
    else:
        form = AppointmentForm(instance=appointment)
    return render(request, 'appointments/form.html', {'form': form})