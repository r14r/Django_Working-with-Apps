from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'email_verified', 'is_staff')
    list_filter = ('role', 'email_verified', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        ('Extra', {'fields': ('role', 'email_verified', 'email_verification_token')}),
    )
