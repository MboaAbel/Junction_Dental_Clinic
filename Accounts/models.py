from django.db import models
from .managers import UserManager
# from django.utils.translation import gettext_lazy as _
# from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db.models import Q
from .constants import PATIENT_TYPE_CHOICES, SPECIALIZATION_CHOICES, GENDER_CHOICES
import string
import random
from django.urls import reverse


def generate_service_id():
    alphanumeric = string.ascii_uppercase + string.digits
    return ''.join(random.choices(alphanumeric, k=6))

# Create a Custom User Model


class User(AbstractUser):
    class RoleChoices(models.TextChoices):
        DOCTOR = "doctor", "Doctor"
        PATIENT = "patient", "Patient"

    
    
    role = models.CharField(choices=RoleChoices.choices,max_length=20,default="patient",error_messages={"required": "Role must be provided"},)
    username = models.CharField(unique=True, null=False, max_length=50, blank=False)
    email = models.EmailField(unique=True, null=False, blank=False)
    next_of_kin = models.ForeignKey('NextOfKin', on_delete=models.CASCADE, blank=True, null=True)
    specialization = models.CharField(max_length=19, blank=True, choices=SPECIALIZATION_CHOICES,)
    profile_photo = models.ImageField(upload_to='profile_photos/', null=False, default='icon/bondijunction_dentalclinic_logo-300x258.jpg', blank=False)
    patient_id = models.CharField(max_length=15, unique=True, blank=True, null=True)
    member_code = models.CharField(default=generate_service_id, max_length=6, unique=True)
    # mobile_number = PhoneNumberField(max_length=13, blank=True, null=True, unique=True)
    mobile_number = models.CharField(max_length=13, blank=True, null=True, unique=True)
    registered = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def set_last_login(self):
        self.last_login = timezone.now()
        self.save(update_fields=['last_login'])

    def set_last_logout(self):
        self.last_logout = timezone.now()
        self.save(update_fields=['last_logout'])

    def next_of_kin_name(self):
        if self.has_next_of_kin:
            try:
                next_of_kin = NextOfKin.objects.get(related_patient=self)
                return f"{next_of_kin.kin_first_name} {next_of_kin.kin_last_name}"
            except NextOfKin.DoesNotExist:
                return "None"
        else:
            return "None"

    # Meta class to set metadata options
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.email
    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip() or self.username

    def get_doctor_profile(self):
        """
        Return doctor profile URL
        """
        return reverse(
            "doctors:doctor-profile", kwargs={"username": self.username}
        )


# Create a model for Next of Kin(for a Patient)
class NextOfKin(models.Model):
    RELATIONSHIP_CHOICES = [
        ('', '----------'),
        ('Brother', 'Brother'),
        ('Sister', 'Sister'),
        ('Son', 'Son'),
        ('Daughter', 'Daughter'),
        ('Mother', 'Mother'),
        ('Father', 'Father'),
        ('Aunt', 'Aunt'),
        ('Uncle', 'Uncle'),
        ('Niece', 'Niece'),
        ('Nephew', 'Nephew'),
        ('Cousin', 'Cousin'),
        ('Other close Relative', 'Other close Relative'),
        ('Wife', 'Wife'),
        ('Husband', 'Husband'),
        ('Guardian', 'Guardian'),
    ]

    kin_first_name = models.CharField(max_length=50)
    kin_code = models.CharField(max_length=15, unique=True, blank=True, null=True)
    kin_last_name = models.CharField(max_length=50)
    related_patient = models.ForeignKey(
        User,
        verbose_name='Related Patient',
        on_delete=models.CASCADE,
        limit_choices_to=Q(is_Member_Patient=True) | Q(mobile_number=True)
    )
    relationship = models.CharField(max_length=50, choices=RELATIONSHIP_CHOICES)
    # kin_mobile_number = PhoneNumberField(max_length=13, blank=True, null=True, unique=False)
    kin_mobile_number = models.CharField(max_length=13, blank=True, null=True, unique=False)
    registered = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.kin_first_name} {self.kin_last_name}"

    class Meta:
        verbose_name = "Next of Kin"
        verbose_name_plural = "Next of Kins"





# Create a method to generate a random appointment ID
# Create a model for OTP(One Time Password)


class OTP(models.Model):
    otp_code = models.CharField(max_length=6)
    otp_created = models.DateTimeField(default=timezone.now)
    otp_verified = models.BooleanField(default=False)
    for_email = models.EmailField(null=True, blank=True, default="")

    @classmethod
    def generate_otp(cls):
        return ''.join(random.choices('0123456789', k=6))

    class Meta:
        verbose_name = "OTP"
        verbose_name_plural = "OTPs"

class Profile(models.Model):
    def profile_photo_directory_path(instance, filename):
        return "profile_photos/user_{0}/{1}".format(instance.user.id, filename)

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile"
    )
    registration_number = models.IntegerField(null=True, blank=True)
    about = models.TextField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default="")
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, blank=True)
    price_per_consultation = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    is_available = models.BooleanField(default=True)
    blood_group = models.CharField(
        max_length=5,
        choices=[
            ("A+", "A+"),
            ("A-", "A-"),
            ("B+", "B+"),
            ("B-", "B-"),
            ("O+", "O+"),
            ("O-", "O-"),
            ("AB+", "AB+"),
            ("AB-", "AB-"),
        ],
        blank=True,
        null=True,
    )
    allergies = models.TextField(blank=True, null=True)
    medical_conditions = models.TextField(blank=True, null=True)

    def __str__(self):
        return "Profile of {}".format(self.user.username)
