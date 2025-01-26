from django.db import models
from Accounts.models import User
from Clinic.models import Specialization
from django.utils.text import slugify



# Create your models here.
class DoctorReg(models.Model):
    member = models.OneToOneField(User, on_delete=models.CASCADE,null=True)
    clinic_code = models.CharField(max_length=8)
    clinic_name = models.CharField(max_length=8)
    mobile_number = models.CharField(max_length=11)
    other_specializations_id = models.ManyToManyField(Specialization,)
    reg_date_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    def __str__(self):
        if self.member:
            return f"{self.member.first_name} {self.member.last_name} - {self.mobile_number}"
        else:
            return f"User not associated - {self.mobile_number}"
        
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.member.first_name + self.member.last_name + self.mobile_number)
        super().save(*args, **kwargs)
