from .models import Appointment
import random
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from Clinic.models import Page, Specialization
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime
from Dashboard.models import DoctorReg
from Accounts.models import User
from django.core.mail import send_mail
from .utils import send_sms,send_sms_via_email
import africastalking
from decouple import config
from django.core.mail import send_mail
from datetime import datetime



# def create_appointment(request):
#     doctorview = DoctorReg.objects.all()
#     worry = Specialization.objects.all()
#     page = Page.objects.all()

#     if request.method == "POST":
#         appointment_number = random.randint(100000000, 999999999)
#         full_name = request.POST.get('full_name')
#         email = request.POST.get('email')
#         mobile_number = request.POST.get('mobile_number')
#         date_of_appointment = request.POST.get('date_of_appointment')
#         time_of_appointment = request.POST.get('time_of_appointment')
#         doctor_id = request.POST.get('doctor_id')
#         worry_id = request.POST.get('worry_need')
#         additional_msg = request.POST.get('additional_msg')

#         # Retrieve the DoctorReg instance using the doctor_id
#         doc_instance = DoctorReg.objects.get(id=doctor_id)
#         worry_instance = Specialization.objects.get(id=worry_id)

#         # Validate that date_of_appointment is greater than today's date
#         try:
#             appointment_date = datetime.strptime(date_of_appointment, '%Y-%m-%d').date()
#             today_date = datetime.now().date()

#             if appointment_date <= today_date:
#                 # If the appointment date is not in the future, display an error message
#                 messages.error(request, "Please select a date in the future for your appointment")
#                 return redirect('appointment')  # Redirect back to the appointment page
#         except ValueError:
#             # Handle invalid date format error
#             messages.error(request, "Invalid date format")
#             return redirect('appointment')  # Redirect back to the appointment page

#         # Create a new Appointment instance with the provided data
#         appointment_details = Appointment.objects.create(
#             appointment_number=appointment_number,
#             fullname=full_name,
#             email=email,
#             mobile_number=mobile_number,
#             date_of_appointment=date_of_appointment,
#             time_of_appointment=time_of_appointment,
#             doctor_id=doc_instance,
#             worry_id=worry_instance,
#             additional_msg=additional_msg
#         )
#         try:

#             if User.objects.filter(email=email).exists() and User.objects.filter(mobile_number=mobile_number).exists():
#                 messages.success(request, f'Account exist on Membership Plan . Kindly Login to your Account of email  {email}')
#                 context = {'doctorview': doctorview, 'appointment_details': appointment_details,
#                            'page': page}
#                 return render(request, 'accounts/includes/appointment_success.html', context)
#         except ValueError:
#             messages.error(request, "Account not found")
#             return redirect('register')  # Redirect back to the appointment page
#         messages.success(request, "Your Appointment Request Has Been Sent. We Will Contact You Soon")
#         appointment_details.save()
#         return redirect('register')  # Redirect back to the appointment page
#     context = {'doctorview': doctorview, 'worry': worry,
#                'page': page}
#     return render(request, 'user_profile/includes/appointment_form.html', context)


@login_required(login_url='/accounts/login')
def User_Search_Appointments(request):
    page = Page.objects.all()
    MemberUser = request.user

    if request.method == "GET":
        query = request.GET.get('query', '')
        if query:
            # Filter records where fullname or Appointment Number contains the query
            patient = Appointment.objects.filter(fullname__icontains=query) | Appointment.objects.filter(appointment_number__icontains=query)
            if patient:
                Appointment_History = Appointment.objects.filter(
                    email__icontains=MemberUser) | Appointment.objects.filter(
                    mobile_number__icontains=MemberUser)
                messages.info(request, "Search against " + query)
                context = {'patient': Appointment_History, 'query': query, 'page': page}
                return render(request, 'appointment/search-appointment.html', context)
            else:
                print("No Record Found")
                context = {'page': page}
                return render(request, 'appointment/userbase.html', context)

        # If the request method is not GET
        context = {'page': page}
        return render(request, 'appointment/userbase.html', context)


@login_required(login_url='/accounts/login')
def user_profile_history_appointment(request):
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
        return render(request, 'user_profile/includes/profile.html', context)
    return render(request, 'user_profile/user_profile.html', context)


def View_Appointment_Details(request, id):
    page = Page.objects.all()
    patientdetails = Appointment.objects.filter(id=id)
    context = {'patientdetails': patientdetails,
               'page': page

               }

    return render(request, 'appointment/includes/user_appointment-details.html', context)


@login_required(login_url='/')
def View_Appointment(request):
    try:
        doctor_reg = DoctorReg.objects.get(admin=request.user)
        view_appointment = Appointment.objects.filter(doctor_id=doctor_reg)

        # Pagination
        paginator = Paginator(view_appointment, 5)  # Show 10 appointments per page
        page = request.GET.get('page')
        try:
            view_appointment = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            view_appointment = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            view_appointment = paginator.page(paginator.num_pages)

        context = {'view_appointment': view_appointment}
    except Exception as e:
        # Handle exceptions, such as database errors, gracefully
        context = {'error_message': str(e)}

    return render(request, 'appointment/includes/view_appointment.html', context)


def AppointmentHistoryList(request, id):
    patientdetails = Appointment.objects.filter(id=id)
    context = {'patientdetails': patientdetails

               }
    return render(request, 'dashboard/includes/doctor_appointment_list_details.html', context)



def create_appointment(request):
    doctorview = DoctorReg.objects.all()
    worry = Specialization.objects.all()
    page = Page.objects.all()

    if request.method == "POST":
        appointment_number = random.randint(100000000, 999999999)
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        mobile_number = request.POST.get('mobile_number')
        date_of_appointment = request.POST.get('date_of_appointment')
        time_of_appointment = request.POST.get('time_of_appointment')
        doctor_id = request.POST.get('doctor_id')
        worry_id = request.POST.get('worry_need')
        additional_msg = request.POST.get('additional_msg')

        # Retrieve the DoctorReg and Specialization instances
        doc_instance = DoctorReg.objects.get(id=doctor_id)
        worry_instance = Specialization.objects.get(id=worry_id)

        # Validate the appointment date
        try:
            appointment_date = datetime.strptime(date_of_appointment, '%Y-%m-%d').date()
            today_date = datetime.now().date()

            if appointment_date <= today_date:
                messages.error(request, "Please select a date in the future for your appointment.")
                return redirect('appointment')
        except ValueError:
            messages.error(request, "Invalid date format.")
            return redirect('appointment')

        # Create appointment
        appointment_details = Appointment.objects.create(
            appointment_number=appointment_number,
            fullname=full_name,
            email=email,
            mobile_number=mobile_number,
            date_of_appointment=date_of_appointment,
            time_of_appointment=time_of_appointment,
            doctor_id=doc_instance,
            worry_id=worry_instance,
            additional_msg=additional_msg
        )

        # Send SMS and email notifications
        try:
            subject = "Appointment Confirmation"
            message = (
                f"Dear {full_name},\n\n"
                f"Thank you for scheduling an appointment with us.\n\n"
                f"Appointment Details:\n"
                f"Appointment Number: {appointment_number}\n"
                f"Date: {date_of_appointment}\n"
                f"Time: {time_of_appointment}\n"
                f"Doctor: {doc_instance}\n"
                f"Concern: {worry_instance}\n\n"
                f"We look forward to serving you.\n\n"
                f"Best regards,\n"
                f"Junction Dental Clinic"
            )
            send_mail(
                subject,
                message,
                '{email}',  # Replace with your clinic's email
                [email, 'mboatechnologies@gmail.com'],  # Recipients
                fail_silently=False,
            )
            
            sms_message = (
                f"Hello {full_name},\n"
                f"Your appointment has been confirmed.\n"
                f"Appointment Number: {appointment_number}\n"
                f"Date: {date_of_appointment}\n"
                f"Time: {time_of_appointment}\n"
                f"Doctor: {doc_instance}\n"
                f"Concern: {worry_instance}\n"
                f"Thank you for choosing us!"
            )
            send_sms(mobile_number, sms_message)  # Assuming send_sms is implemented correctly

            
            messages.success(request, "Appointment confirmed. Notifications sent successfully.")
        except Exception as e:
            messages.error(request, f"Failed to send notifications: {str(e)}")

        return redirect('appointment_success')  # Redirect to a success page

    context = {'doctorview': doctorview, 'worry': worry, 'page': page}
    return render(request, 'user_profile/includes/appointment_form.html', context)


def send_sms(phone_number, message):
    try:
        username = 'Junction_Dental'
        api_key = 'your_api_key_here'  # Replace with environment variable
        africastalking.initialize(username, api_key)
        sms = africastalking.SMS
        sms.send(message, [phone_number])
    except Exception as e:
        raise Exception(f"SMS sending failed: {str(e)}")


def appointment_success(request):
    return render(request, 'accounts/includes/appointment_success.html',)
