from django.contrib import admin
from .models import Appointment

# Register your models here.

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'patient', 'appointment_date', 'status')
    list_filter = ('status', 'appointment_date')
    search_fields = ('doctor__username', 'patient__username')

admin.site.register(Appointment, AppointmentAdmin)