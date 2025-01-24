from django.shortcuts import render, redirect
from .forms import UserProfileUpdateForm, RegistrationForm, LoginForm, UserPasswordResetForm, UserSetPasswordForm, \
    UserPasswordChangeForm
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView, PasswordChangeView
from django.contrib.auth import logout
from .models import User
from Clinic.models import Page
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from Clinic.models import Specialization
from Appointment.models import Appointment


# Create your views here.

def index(request):
    return render(request, 'accounts/sign-up.html')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            print("Account created successfully!")
            return redirect('/accounts/login/')
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
    return redirect('/accounts/login/')


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


# def user_profile(request):
#     user_view = request.user
#     page = Page.objects.all()
#     Services = Specialization.objects.all()
#     context = {'services': Services, 'page': page}
#     Appointment_History = Appointment.objects.filter(email__icontains=user_view) | Appointment.objects.filter(
#         mobile_number__icontains=user_view)
#     if Appointment_History:
#         # Filter records where fullname or Appointment Number contains the query
#         Appointee = Appointment_History
#         messages.info(request, 'Your Appointment History Exists')
#         context = {'Appointee': Appointee, 'user_view': user_view, 'page': page, 'services': Services, }
#         return render(request, 'dashboard/includes/profile.html', context)
#     return render(request, 'user_profile/includes/profile.html', context)


from django.db.models import Q

def user_profile(request):
    user_view = request.user
    page = Page.objects.all()
    services = Specialization.objects.all()
    
    # Get appointments based on user type
    if user_view.is_staff:
        appointments = Appointment.objects.all()
    else:
        appointments = Appointment.objects.filter(
            Q(email=user_view.email) | 
            Q(mobile_number=user_view.mobile_number)
        ).order_by('-created_at')
    
    context = {
        'user_view': user_view,
        'page': page,
        'services': services,
        'appointments': appointments,
    }
    
    if appointments.exists():
        messages.info(request, 'Your Appointment History')
        return render(request, 'dashboard/includes/profile.html', context)
    else:
        messages.info(request, 'No Appointment History Found')
        return render(request, 'user_profile/includes/profile.html', context)

@login_required(login_url='/accounts/login')
def profile_Update_shit(request):
    form = UserProfileUpdateForm()
    member = User.objects.get(email=request.user)
    if request.method == 'POST':
        if request.FILES.get('image') is not None:
            profile_photo = member.profile_photo
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            phone_number = request.POST.get('phone_number')
            username = request.POST.get('username')
            try:
                if request.FILES.get('image') is None:
                    profile_photo = request.FILES.get('profile_picture')

                member.profile_photo = profile_photo
                member.phone_number = phone_number
                member.first_name = first_name
                member.username = username
                member.email = email
                member.last_name = last_name
                member.save()
                context = {'member': member}

            except:
                messages.error(request, "Your profile updation has been failed")
                return render(request, 'user_profile/includes/user_profile_update.html')
        return render(request, 'user_profile/includes/user_profile_update.html', context)


@login_required(login_url='/accounts/login')
def profile_Update(request):
    member_profile = User.objects.all()
    form = UserProfileUpdateForm()
    if request.method == 'POST':
        profile_photo = member_profile.profile_photo
        first_name = member_profile.first_name
        second_name = member_profile.last_name
        specialization = member_profile.specialization
        is_Doctor = member_profile.is_Doctor
        next_of_kin = member_profile.next_of_kin
        has_next_of_kin = member_profile.has_next_of_kin
        is_Member_Patient = member_profile.is_Member_Patient
        email = member_profile.email
        username = member_profile.username
        patient_type = member_profile.patient_type
        patient_id = member_profile.patient_id
        member_code = member_profile.member_code
        gender = member_profile.gender
        mobile_number = member_profile.mobile_number
        registered = member_profile.registered

        member_profile.profile_photo = profile_photo
        member_profile.first_name = first_name
        member_profile.second_name = second_name
        member_profile.specialization = specialization
        member_profile.registered = registered
        member_profile.mobile_number = mobile_number
        member_profile.member_code = member_code
        member_profile.gender = gender
        member_profile.patient_type = patient_type
        member_profile.patient_id = patient_id
        member_profile.is_Doctor = is_Doctor
        member_profile.next_of_kin = next_of_kin
        member_profile.has_next_of_kin = has_next_of_kin
        member_profile.is_Member_Patient = is_Member_Patient
        member_profile.email = email
        member_profile.username = username
        member_profile.save()
        return render(request, 'user_profile/includes/profile.html')

    return render(request, 'user_profile/includes/user_profile_update.html', {'form': form})
