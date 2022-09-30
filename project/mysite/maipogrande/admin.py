from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import (
    Contact, CustomUser, Profile, Post, Relationship,

    Contract, ProductRequest, ProductRequestStatus, BankAccount
)

class CustomUserAdmin(UserAdmin):
    list_display = (
        'username', 'email', 'first_name', 'last_name', 'is_staff',
        'type',
    )

    fieldsets = (
        (None, {
            'fields': ('username', 'password',)
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email',)
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions',
                )
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined',)
        }),
        ('Additional info', {
            'fields': ('type',)
        })
    )

    add_fieldsets = (
        (None, {
            'fields': ('username', 'password1', 'password2',)
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email',)
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions',
                )
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined',)
        }),
        ('Additional info', {
            'fields': ('type',)
        })
    )

admin.site.register(CustomUser, CustomUserAdmin)

admin.site.register(Profile)
admin.site.register(Relationship)
admin.site.register(Post)
admin.site.register(Contract)
admin.site.register(ProductRequest)
admin.site.register(ProductRequestStatus)
admin.site.register(BankAccount)
admin.site.register(Contact)