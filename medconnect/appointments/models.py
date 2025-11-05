from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth import get_user_model
from notifications.models import Notification

User = get_user_model()
# Create your models here.
class Appointment(models.Model):
    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="appointments"
    )
    doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="doctor_appointments"
    )
    date = models.DateField()
    time = models.TimeField()
    reason = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=[
            ('scheduled', 'Scheduled'),
            ('completed', 'Completed'),
            ('cancelled', 'Cancelled'),
        ],
        default='scheduled'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Appointment with Dr. {self.doctor.username} on {self.date}"

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]

    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctor_appointments', limit_choices_to={'role': 'doctor'})
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patient_appointments', limit_choices_to={'role': 'patient'})
    appointment_date = models.DateTimeField()
    symptoms = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    is_reminder_sent = models.BooleanField(default=False)
    time = models.TimeField(max_length=50)
    time_slot = models.CharField(max_length=50, choices=[
        ('09:00-10:00', '09:00-10:00'),
        ('10:00-11:00', '10:00-11:00'),
        ('11:00-12:00', '11:00-12:00'),
        ('12:00-13:00', '12:00-13:00'),
        ('13:00-14:00', '13:00-14:00'),
        ('14:00-15:00', '14:00-15:00'),
        ('15:00-16:00', '15:00-16:00'),
        ('16:00-17:00', '16:00-17:00'),
    ])

    def __str__(self):
        return f"{self.patient.username} with Dr. {self.doctor.username} on {self.appointment_date.strftime('%Y-%m-%d %H:%M')}"

    class Meta:
        ordering = ['-appointment_date']

def create_appointment_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.doctor,
            message=f"New appointment scheduled with {instance.patient.username} on {instance.date} at {instance.time}."
        )

from django.db.models.signals import post_save
post_save.connect(create_appointment_notification, sender=Appointment)