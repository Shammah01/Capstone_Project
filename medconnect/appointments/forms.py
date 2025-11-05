from django import forms
from .models import Appointment

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['doctor', 'appointment_date', 'symptoms', 'status', 'patient', 'time', 'time_slot']
        widgets = {
            'appointment_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'time_slot': forms.TimeInput(attrs={'type': 'time'}),
        }
