from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, NextOfKin, OTP, Profile
# Create a custom user admin class
admin.site.register(User)


class User(admin.ModelAdmin):
    list_display = [
        'username', 'first_name', 'last_name', 'email', 'mobile_number', 'last_login',
        'last_logout', 'active', ]
    list_filter = (
        'is_Member_Patient', 'is_New_Patient', 'is_Doctor', 'next_of_kin', 'username',
        'has_next_of_kin', 'first_name', 'last_name', 'email', 'patient_id', 'gender', 'mobile_number',
        'specialization',)
    search_fields = (
        'username', 'first_name', 'last_name', 'email', 'specialization', 'gender', 'phone_number', 'patient_id')
    ordering = ('mobile_number',)

    actions = ['deactivate_users', 'activate_users']
    def deactivate_users(self, request, queryset):
        queryset.update(active=False)

    deactivate_users.short_description = "Deactivate selected users"

    def activate_users(self, request, queryset):
        queryset.update(active=True)

    activate_users.short_description = "Activate selected users"

    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'Custom Field Heading',
            {
                'fields': (
                    'is_Student_Patient',
                    'is_Staff_Patient',
                    'is_Doctor',
                )
            }
        )
    )

admin.site.register(Profile)
admin.site.register(NextOfKin)


class NextOfKinAdmin(admin.ModelAdmin):
    list_display = ('kin_fname', 'kin_lname', 'related_patient', 'relationship', 'kin_mobile_number')
    list_filter = ('kin_fname', 'kin_lname', 'related_patient', 'relationship', 'kin_mobile_number')
    search_fields = ('kin_fname', 'kin_lname', 'related_patient', 'relationship', 'kin_mobile_number')


admin.site.register(OTP)


class OTPAdmin(admin.ModelAdmin):
    list_display = ('otp_code', 'otp_created', 'otp_verified', 'for_email')
    list_filter = ('otp_code', 'otp_verified', 'otp_created', 'for_email',)
    search_fields = ('otp_code', 'otp_verified', 'otp_created', 'for_email')
    readonly_fields = ('otp_code', 'otp_created', 'otp_verified', 'for_email')
