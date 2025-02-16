from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    CustomUser
)


# Custom User Admin (Jazzmin Optimized)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'is_active', 'is_staff', 'date_joined')
    search_fields = ('username', 'email', 'role')
    list_filter = ('role', 'is_active', 'is_staff', 'is_superuser')
    ordering = ('-date_joined',)
    fieldsets = (
        ('User Details', {'fields': ('username', 'email', 'password', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        ('Create User', {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role'),
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)
