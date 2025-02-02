from urllib import request
from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserProfileUpdateForm, User_ProfileUpdateForm, RegistrationForm, LoginForm, UserPasswordResetForm, UserSetPasswordForm, \
    UserPasswordChangeForm
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView, PasswordChangeView
from django.contrib.auth import logout
from .models import User
from Clinic.models import Page
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from Clinic.models import Specialization
from Appointment.models import Appointment
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from utils.htmx import render_toast_message_for_api
from Dashboard.models import DoctorReg
from bookings.models import Booking
from django.db.models import Q
from django.urls import reverse_lazy
from mixins.custom_mixins import PatientRequiredMixin
from django.views.generic import UpdateView

# Create your views here.

def index(request):
    return render(request, 'accounts/sign-up.html')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            print("Account created successfully!")
            return redirect('/Accounts/login/')
        else:
            print("Registration failed!")
    else:
        form = RegistrationForm()

    context = {'form': form}
    return render(request, 'accounts/sign-up.html', context)


class UserLoginView(LoginView):
    template_name = 'accounts/sign-in.html'
    form_class = LoginForm


class UserPasswordResetView(PasswordResetView):
    template_name = 'accounts/includes/password_reset.html'
    form_class = UserPasswordResetForm


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/includes/password_reset_confirm.html'
    form_class = UserSetPasswordForm


class UserPasswordChangeView(PasswordChangeView):
    template_name = 'accounts/includes/password_change.html'
    form_class = UserPasswordChangeForm


def user_logout_view(request):
    logout(request)
    return render(request, 'accounts/includes/logged_out.html')


def user_profile_view(request):
    user_view = request.user
    page = Page.objects.all()
    Services = Specialization.objects.all()
    context = {'services': Services, 'page': page}
    Appointment_History = Appointment.objects.filter(email__icontains=user_view) | Appointment.objects.filter(
        mobile_number__icontains=user_view)
    if Appointment_History:
        # Filter records where fullname or Appointment Number contains the query
        Appointee = Appointment_History
        messages.info(request, 'Your Appointment History Exists')
        context = {'Appointee': Appointee, 'user_view': user_view, 'page': page, 'services': Services, }
        return render(request, 'user_profile/includes/user_profile.html', context)
    return render(request, 'user_profile/includes/user_profile.html', context)



@login_required(login_url='/Accounts/login')
def user_profile(request):
    user_view = request.user
    page = Page.objects.all()
    services = Specialization.objects.all()
    doctor = User.objects.filter(email=user_view,role=User.RoleChoices.DOCTOR)
    
    # Get appointments based on user type
    if user_view.is_staff:
        appointments = (Appointment.objects
        .select_related("appointee", "doctor_id")
        .filter(status="0"))
        Bookings = Booking.objects.all()
        doctors = DoctorReg.objects.all() 
        context = {
        'user_view': doctor,
        'appointments': appointments,
        'doctors':doctors,
        'bookings':Bookings,
    } 
        
        return render(request, 'bookings/booking.html', context)

    else:
        appointments = Appointment.objects.filter(
            Q(email=user_view.email) | 
            Q(mobile_number=user_view.mobile_number) |
            Q(fullname=user_view.get_full_name)
        ).order_by('-created_at')
    
    context = {
        'user_view': user_view,
        'page': page,
        'services': services,
        'appointments': appointments,
        'doctor':doctor,
    }
    
    if appointments.exists():
        return render(request, 'dashboard/includes/profile.html', context)
    else:
        messages.info(request, 'No Appointment History Found')
        return render(request, 'user_profile/includes/profile.html', context)


@login_required(login_url='/Accounts/login')
def profile_Update(request):
    page = Page.objects.all()
    patient = get_object_or_404(User, username=request.user.username, role=User.RoleChoices.PATIENT)
    
    form = UserProfileUpdateForm()
    form_2 = User_ProfileUpdateForm()
    return render(request, 'user_profile/includes/user_profile_update.html', {'form': form, 'form_1':form_2,'page': page,'patient':patient,} )


@login_required(login_url='/Accounts/login')
class UpdateBasicUserInformationAPIView(UserPassesTestMixin):
    template_name = 'user_profile/user_profile-update.html'
    form_class = UserProfileUpdateForm


    def get_object(self):
        return self.request.user

    def put(self, request, *args, **kwargs):
        try:
            user = request.user
            data = request.POST
            files = request.FILES

            # Update user information
            user.first_name = data.get("first_name", user.first_name)
            user.last_name = data.get("last_name", user.last_name)
            user.save()

            # Update profile information
            user_profile = user.profile
            user_profile.registration_number = data.get("registration_number")
            user_profile.gender = data.get("gender")

            # Handle avatar file upload
            if "avatar" in files:
                user.profile_photo = files["profile_photo"]

            user_profile.save()

            return render_toast_message_for_api(
                "Information", "Updated successfully", "success"
            )
        except Exception as e:
            return render_toast_message_for_api("Error", str(e), "error")

class PatientProfileUpdateView(PatientRequiredMixin, UpdateView):
    model = User
    template_name = "user_profile/includes/use_profile_update.html"
    success_url = reverse_lazy("user_profile")
    form_class = UserProfileUpdateForm

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        user = form.save(commit=False)
        profile = user.profile

        # Handle profile image upload
        if self.request.FILES.get("avatar"):
            profile.image = self.request.FILES["avatar"]

        # Update profile fields
        profile_fields = [
            "blood_group",
            "gender",
            "medical_conditions",
            "allergies",
            "address",
            "city",
            "state",
            "postal_code",
            "country",
        ]

        for field in profile_fields:
            value = self.request.POST.get(field)
            if value:
                setattr(profile, field, value)

        # Save both user and profile
        user.save()
        profile.save()

        messages.success(self.request, "Profile updated successfully")
        return redirect(self.success_url)

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
