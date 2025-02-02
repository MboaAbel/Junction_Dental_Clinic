from django.urls import path
from. import views
from .views  import (AppointmentCancelView,AppointmentPrintView,AppointmentDetailView
)



urlpatterns = [
        path('appointment_success/<str:appointment_number>/', views.appointment_success, name='appointment_success'),
        path('User_Appointment/', views.create_appointment, name='appointment'),
        path('User_SearchAppointment', views.User_Search_Appointments, name='user_search_appointment'),
        path('ViewAppointmentDetails/<str:id>/', views.View_Appointment_Details, name='view_appointment_details'),
        path('ViewAppointment/', views.View_Appointment, name='view_appointment'),
        path("appointments/<int:pk>/cancel/",AppointmentCancelView.as_view(),name="appointment-cancel",),
        path("appointments/<int:pk>/print/",AppointmentPrintView.as_view(),name="appointment-print",),
        path("appointments/<int:pk>/",AppointmentDetailView.as_view(),name="appointment-detail",),

]

