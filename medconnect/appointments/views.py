# Create your views here.

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Appointment
from .forms import AppointmentForm

@login_required
def book_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user
            appointment.save()
            return redirect('appointment_list')
    else:
        form = AppointmentForm()
    return render(request, 'appointment/book_appointment.html', {'form': form})

@login_required
def appointment_list(request):
    if request.user.role == 'doctor':
        appointments = Appointment.objects.filter(doctor=request.user)
    else:
        appointments = Appointment.objects.filter(patient=request.user)
    return render(request, 'appointment/appointment_list.html', {'appointments': appointments})
