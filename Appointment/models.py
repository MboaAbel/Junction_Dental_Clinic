from django.db import models
from Clinic.models import Specialization
from Accounts.models import User
from Accounts.constants import *
from Dashboard.models import DoctorReg


class Appointment(models.Model):

    nerd = models.CharField(max_length=50, null=True,blank=True) # on creating an appointment by actual filling the form. can be a bot,admin,staff,or you 
    appointment_number = models.IntegerField(default=0, null='TRUE')
    appointee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patients', null=True, blank=False)
    fullname = models.CharField(max_length=250)
    mobile_number = models.CharField(max_length=11)
    email = models.EmailField(max_length=100)
    date_of_appointment = models.CharField(max_length=250)
    time_of_appointment = models.CharField(max_length=250)
    doctor_id = models.ForeignKey(DoctorReg, blank=True, null=True, on_delete=models.CASCADE)
    worry_id = models.ForeignKey(Specialization, on_delete=models.CASCADE, default=0, null=False)
    additional_msg = models.TextField(blank=True)
    remark = models.CharField(max_length=250, default=0)
    status = models.CharField(default=0, max_length=200)
    prescription = models.TextField(blank=True, default=0)
    recommended_test = models.TextField(blank=True, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    appoint_status = models.CharField('Status', max_length=10, null=True, choices=APPOINTMENT_STATUS_CHOICES, blank=False, )
    payment = models.BooleanField('Payment', default=False, blank=True, null=True, choices=PAYMENT_CHOICES)

    def __str__(self):
        return f"{self.appointment_number}"

