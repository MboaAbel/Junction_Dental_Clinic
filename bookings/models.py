from django.db import models
from django.conf import settings
from ckeditor.fields import RichTextField
from Accounts.models import User
from Appointment.models import Appointment


class Booking(models.Model):
     # Helps manage Apppointment identity by linking an appointment to a user.
    appointment_ok = models.ForeignKey(
        Appointment,
        on_delete=models.CASCADE,
        related_name="booking",
        limit_choices_to={"status": "0"},
    )
    doctor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="appointments",
        limit_choices_to={"role": "doctor"},
    )
    patient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        related_name="patient_appointments",
        limit_choices_to={"role": "patient"},
    )
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    booking_date = models.DateTimeField(auto_now_add=True)
    symptoms = models.TextField(null=True,blank=True)
    diagnosis = models.TextField(null=True,blank=True)
    medications = RichTextField(null=True,blank=True)
    notes = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    nerd = models.CharField(max_length=50, null=True,blank=True)
    #this status is mainly done by recepion and doctor. The result is send to a user as update.sms,email,in app notification
    status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "Pending"),
            ("confirmed", "Confirmed"),
            ("completed", "Completed"),
            ("cancelled", "Cancelled"),
            ("scheduled", "Scheduled"),
        ],
        default="pending",
    )

    class Meta:
        ordering = ["-appointment_date", "-appointment_time"]
        # Ensure no double bookings for same doctor at same time
        unique_together = ["doctor","appointment_ok", "appointment_date", "appointment_time"]

    def __str__(self):
        return f"Appointment for {self.patient} with Dr. {self.doctor.get_full_name()} on {self.appointment_date} at {self.appointment_time}"
    


