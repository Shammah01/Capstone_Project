# Create your views here.

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Appointment
from .forms import AppointmentForm
from notifications.models import Notification

@login_required
def appointment_list(request):
    appointments = Appointment.objects.filter(user=request.user).order_by('-date')
    return render(request, 'appointments/appointment_list.html', {'appointments': appointments})

@login_required
def appointment_create(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.user = request.user
            appointment.save()
            Notification.objects.create(
                user=request.user,
                appointment=appointment,
                message=f"Your appointment with {appointment.doctor_name} on {appointment.date} has been booked!"
            )
            
            return redirect('appointment_list')
    else:
        form = AppointmentForm()
    return render(request, 'appointments/appointment_form.html', {'form': form})

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
    return render(request, 'appointments/book_appointment.html', {'form': form})

@login_required
def cancel_appointment(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk, patient=request.user)
    appointment.status = 'cancelled'
    appointment.save()
    Notification.objects.create(
        user=appointment.doctor,
        message=f"The appointment with {appointment.patient.username} on {appointment.appointment_date} has been cancelled."
    )
    return redirect('appointment_list')