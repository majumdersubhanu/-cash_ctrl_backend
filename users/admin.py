from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from .models import User


class UserAdmin(BaseUserAdmin):
    # Add 'date_joined' to readonly_fields to make it visible but not editable
    readonly_fields = ('last_login', 'date_joined','profile_picture')

    def profile_picture(self, obj):
        if obj.profile_pic:
            return format_html('<img src="{}" width="100" height="100" />', obj.profile_pic.url)
        return "No picture uploaded"

    profile_picture.short_description = 'Profile Picture'  # Optional

    # Ensure all your model fields are accounted for in fieldsets for detail view
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal Information'), {'fields': (
        'full_name', 'email', 'phone_number', 'date_of_birth', 'gender', 'current_address', 'nationality')}),
        (_('Employment Details'), {'fields': ('job_title', 'company_name', 'employment_status', 'monthly_income')}),
        (_('Financial Information'), {'fields': ('account_number', 'ifsc_code', 'bank_name', 'upi_id')}),
        (_('Identification Documents'), {'fields': ('pan_card', 'aadhaar_card')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined',)}),
        ('Other Information', {'fields': ('profile_picture',)}),
    )

    # Use this to define fields when adding a user (You might not want all fields here)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'phone_number', 'password1', 'password2'),
        }),
        (_('Personal Information'),
         {'fields': ('full_name', 'date_of_birth', 'gender', 'current_address', 'nationality')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )

    # Customize which fields are displayed in the user list
    list_display = ('username', 'email', 'phone_number', 'full_name', 'is_staff', 'date_joined')

    # Fields to filter the users by in the admin panel (customize as needed)
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'gender', 'nationality')

    # Fields to search users by in the admin panel
    search_fields = ('username', 'email', 'full_name', 'phone_number')

    # Default ordering of users in the admin panel
    ordering = ('email',)


admin.site.register(User, UserAdmin)
