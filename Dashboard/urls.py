from django.urls import path
from .views.dashboard_view import *

urlpatterns = [


    path('', Dashboard_view, name='doctor_home'),
    path('mpesa', mpesa, name='mpesa'),
    path('member', member, name='member'),
    path('table', records, name='table'),
    path('DoctorSignup', DoctorSignup, name='Doctor_registration'),
    path('ViewAppointments', View_Appointment, name='view_appointment'),
    path('Create', create_appointment, name='dashboard_create_appointment'),
    path('PatientAppointmentDetails/<str:id>', Patient_Appointment_Details,name='patientappointmentdetails'),
    path('AppointmentDetailsRemark/Update', Patient_Appointment_Details_Remark, name='patient_appointment_details_remark'),
    path('DoctorPatientApprovedAppointment', Patient_Approved_Appointment, name='patient_approved_appointment'),
    path('DoctorPatientCancelledAppointment', Patient_Cancelled_Appointment, name='patient_cancelled_appointment'),
    path('DoctorPatientNewAppointment', Patient_New_Appointment, name='patient_new_appointment'),
    path('DoctorPatientListApprovedAppointment', Patient_List_Approved_Appointment,name='patient_list_appointment'),
    path('DoctorAppointmentList/<str:id>', DoctorAppointmentList, name='doctor_appointment_list'),
    path('PatientAppointmentPrescription', Patient_Appointment_Prescription,name='patientappointmentprescription'),
    path('PatientAppointmentCompleted', Patient_Appointment_Completed, name='patient_appointment_completed'),
    path('SearchAppointment', Search_Appointments, name='search_appointment'),
    path('BetweenDateReport', Between_Date_Report, name='between_date_report'),
]
