from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'full_name', 'is_verified', 'is_staff', 'is_active', 'created_at', 'actions_column')
    list_filter = ('is_verified', 'is_staff', 'is_superuser', 'is_active', 'created_at', 'date_joined')
    search_fields = ('email', 'username', 'first_name', 'last_name', 'phone_number')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at', 'date_joined', 'last_login', 'password_change_date')
    
    fieldsets = (
        ('Authentication', {
            'fields': ('username', 'password', 'email'),
            'classes': ('wide',)
        }),
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'phone_number'),
            'classes': ('wide',)
        }),
        ('Permissions & Status', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'is_verified', 'groups', 'user_permissions'),
            'classes': ('wide',)
        }),
        ('Important Dates', {
            'fields': ('last_login', 'date_joined', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    add_fieldsets = (
        ('Create New User', {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )
    
    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    full_name.short_description = 'Full Name'
    
    def password_change_date(self, obj):
        if obj.last_login:
            return obj.last_login.strftime('%Y-%m-%d %H:%M:%S')
        return 'Never'
    password_change_date.short_description = 'Last Login'
    
    def actions_column(self, obj):
        return format_html(
            '<a class="button" href="{}">View Profile</a>',
            reverse('admin:users_user_change', args=[obj.pk])
        )
    actions_column.short_description = 'Actions'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related()
    
    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }
        js = ('admin/js/custom_admin.js',)
