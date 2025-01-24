from django.urls import path
from . import views

app_name = 'appointment'

urlpatterns = [
        path('appointment_success/<str:appointment_number>/', views.appointment_success, name='appointment_success'),
        path('Booking/User_Appointment/', views.create_appointment, name='appointment'),
        path('Booking/User_SearchAppointment', views.User_Search_Appointments, name='user_search_appointment'),
        path('Booking/User_SearchAppointment', views.User_Search_Appointments, name='user_search_appointment'),
        path('Booking/ViewAppointmentDetails/<str:id>/', views.View_Appointment_Details, name='view_appointment_details'),
        path('Booking/ViewAppointmentDetails/<str:id>/', views.View_Appointment_Details, name='view_appointment_details'),
        path('Booking/ViewAppointmentDetails/<str:id>/', views.View_Appointment_Details, name='view_appointment_details'),
        path('Booking/ViewAppointment/', views.View_Appointment, name='view_appointment'),

]

