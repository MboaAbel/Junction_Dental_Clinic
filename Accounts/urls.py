from django.urls import path
from . import views
from django.contrib.auth import views as auth_views 

urlpatterns = [
    # Authentication
    path('profile_update', views.UpdateBasicUserInformationAPIView, name='update-basic-information'),
    path('profile/update',views.profile_Update,name='user_profile_update'),
    path('profile/', views.user_profile, name='user_profile'),
    path('profile/view', views.user_profile_view, name='user_profile_view'),
    path("profile-settings/",views.PatientProfileUpdateView.as_view(),name="profile-setting",),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.user_logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('password-change/', views.UserPasswordChangeView.as_view(), name='password_change'),
    path('password-change-done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='accounts/includes/password_change_done.html'
    ), name="password_change_done"),
    path('password-reset/', views.UserPasswordResetView.as_view(), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/',
         views.UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset-done/', auth_views.PasswordResetDoneView.as_view(
        template_name='accounts/includes/password_reset_done.html'
    ), name='password_reset_done'),
    path('includes/password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='accounts/includes/password_reset_complete.html'
    ), name='password_reset_complete'),
]
