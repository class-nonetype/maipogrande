

from .models import (
    Contact,
    CustomUser,
    Profile,
    Product,
    Relationship,
    Transport,
    Contract,
    ProductRequest,
    ProductRequestStatus,
    BankAccount,
    Transaction,
    TransportRequestStatus
)

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


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

# 
###################################################################
#   Agregar el modelo instanciado para que en el panel            #          
#   de administracion se vean reflejadas las clases de modelos    #
###################################################################
admin.site.register(CustomUser, CustomUserAdmin)

admin.site.register(Profile)
admin.site.register(Relationship)
admin.site.register(Product)
admin.site.register(Contract)
admin.site.register(Transport)
admin.site.register(ProductRequest)
admin.site.register(ProductRequestStatus)
admin.site.register(Contact)
admin.site.register(Transaction)
admin.site.register(BankAccount)
admin.site.register(TransportRequestStatus)
