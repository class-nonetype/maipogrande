from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import (
    Contact, CustomUser, Post, Contract, BankAccount, ProductRequest,

    USER_TYPE, TYPE_BANK_ACCOUNT, BANK_NAMES, CONTRACT_STATUS, ANSWER
)

from django.core.validators import MinValueValidator, MaxValueValidator

import datetime

class SignUpForm(UserCreationForm):
    
    first_name = forms.CharField(label='Nombres', widget = forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='Apellidos', widget = forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label = 'E-mail',widget = forms.EmailInput(attrs={'class': 'form-control'}))
    username = forms.CharField(label = 'Nombre de Usuario', widget = forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Contraseña', widget = forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Confirma la contraseña', widget = forms.PasswordInput(attrs={'class': 'form-control'}))
    type = forms.ChoiceField(
    	choices=USER_TYPE, required=True,
    	label = 'Selecciona el tipo de usuario a crear',
    	widget = forms.Select(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = CustomUser
        fields = UserCreationForm.Meta.fields + (
            'type', 'email',
			'username', 'password1', 'password2',
			'first_name', 'last_name',
        )
    
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)


class PostForm(forms.ModelForm):
    
    title = forms.CharField(label = 'Titulo', widget = forms.TextInput(attrs={'class': 'form-control', 'rows':2, 'placeholder': 'Ej: Manzana'}), required=True)
    description = forms.CharField(label = 'Descripcion', widget = forms.Textarea(attrs={'class': 'form-control', 'rows':2, 'placeholder': 'Agrega una descripcion'}), required=True)
    price = forms.IntegerField(label = 'Precio (kg)', widget = forms.NumberInput(attrs={'class': 'form-control', 'type':'number' }), required=True, max_value=1000000000, min_value=1000)
    quantity = forms.IntegerField(
        label = 'Cantidad (kg)', max_value=1000, min_value=1,
        widget = forms.NumberInput(attrs={'class': 'form-control', 'type':'number'})
    )
    image = forms.ImageField(label = 'Selecciona la imagen', widget = forms.FileInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = Post
        fields = ['title', 'price', 'quantity', 'description', 'image']

class ContactForm(forms.ModelForm):
    first_name = forms.CharField(label = 'Nombres', widget = forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label = 'Apellidos', widget = forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label = 'E-mail',widget = forms.EmailInput(attrs={'class': 'form-control'}))
    subject = forms.CharField(label = 'Asunto', widget = forms.TextInput(attrs={'class': 'form-control'}))
    text = forms.CharField(label = 'Descripcion', widget = forms.Textarea(attrs={'class': 'form-control'}))
    
    class Meta:
        
        model = Contact
        
        fields = [
            'first_name', 'last_name', 'email', 'subject', 'text', 
        ]


class ContractForm(forms.ModelForm):

    image = forms.ImageField(label = 'Selecciona la imagen', widget = forms.FileInput(attrs={'class': 'form-control'}))
    rut = forms.CharField(label = 'Rut', widget = forms.TextInput(attrs={'class': 'form-control', 'rows':2, 'placeholder': 'Ej: 11.111.111-1'}), required=True)
    phono = forms.IntegerField(label = 'Numero de contacto', widget = forms.NumberInput(attrs={'class': 'form-control', 'type':'number' }), required=True)
    issued_date = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M:%S'], widget = forms.DateTimeInput(format='%d/%m/%Y %H:%M:%S', attrs={'class': 'form-control'}))
    contract_closing_date = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M:%S'], widget = forms.DateTimeInput(format='%d/%m/%Y %H:%M:%S', attrs={'class': 'form-control'}))
    status = forms.ChoiceField(
    	choices = CONTRACT_STATUS, required=True,
    	label = 'Selecciona el estado del contrato',
    	widget = forms.Select(attrs={'class': 'form-control'})
    )


    class Meta:
        model = Contract
        fields = ['image', 'rut', 'phono', 'issued_date', 'contract_closing_date']



class BankAccountForm(forms.ModelForm):
    bank_name = forms.ChoiceField(
        choices = BANK_NAMES, required = True,
        label = 'Selecciona el nombre del banco',
        widget = forms.Select(attrs={'class': 'form-control'})
    )
    type_bank_account = forms.ChoiceField(
        choices = TYPE_BANK_ACCOUNT, required = True,
        label = 'Selecciona el tipo de cuenta',
        widget = forms.Select(attrs={'class': 'form-control'})
    )
    bank_account_number = forms.IntegerField(
        label = 'Numero de Cuenta',
        widget = forms.NumberInput(attrs={'class': 'form-control', 'type':'number', 'placeholder' : 'Ej : 11222333'}),
        required=True)
    owner_full_name = forms.CharField(label = 'Nombre completo del titular', widget = forms.TextInput(attrs={'class': 'form-control', 'rows':2, 'placeholder': 'Ingresa el nombre completo del titular'}), required=True)
    
    class Meta:
        model = BankAccount
        fields = ['bank_name', 'type_bank_account', 'bank_account_number', 'owner_full_name']


'''
CLIENTE EXTERNO
'''

class ProductRequestForm(forms.ModelForm):


    title = forms.CharField(label = 'Titulo', widget = forms.TextInput(attrs={'class': 'form-control', 'rows':2, 'placeholder': 'Ej: Manzana'}), required=True)
    description = forms.CharField(label = 'Descripcion', widget = forms.Textarea(attrs={'class': 'form-control', 'rows':2, 'placeholder': 'Agrega una descripcion'}), required=True)
    quantity = forms.IntegerField(
        label = 'Cantidad (kg)', max_value=1000, min_value=1,
        widget = forms.NumberInput(attrs={'class': 'form-control', 'type':'number'})
    )
    requested_date = forms.DateField(
        label = 'Fecha solicitada',
        input_formats=['%d/%m/%Y'],
        initial = datetime.date.today(),
        widget = forms.SelectDateWidget(attrs = {'class': 'form-control snps-inline-select'})
    )
    temperature_care = forms.ChoiceField(
    	choices = ANSWER, required = True,
    	label = 'Se necesita de un cuidado de temperatura?',
    	widget = forms.Select(attrs={'class': 'form-control'})
    )
    class Meta:
        model = ProductRequest
        fields = ['title', 'description', 'quantity', 'requested_date', 'temperature_care']



class ProductRequestStatusForm(forms.ModelForm):

    offer = forms.CharField(label = 'Producto ofrecido', widget = forms.TextInput(attrs={'class': 'form-control', 'rows':2, 'placeholder': 'Ej: Manzana'}), required=True)
    description = forms.CharField(label = 'Descripcion', widget = forms.Textarea(attrs={'class': 'form-control', 'rows':2, 'placeholder': 'Agrega una descripcion'}), required=True)
    quantity = forms.IntegerField(
        label = 'Cantidad (kg)', max_value=1000, min_value=1,
        widget = forms.NumberInput(attrs={'class': 'form-control', 'type':'number'})
    )
    requested_date = forms.DateField(
        label = 'Fecha solicitada',
        input_formats=['%d/%m/%Y'],
        initial = datetime.date.today(),
        widget = forms.SelectDateWidget(attrs = {'class': 'form-control snps-inline-select'})
    )
    temperature_care = forms.ChoiceField(
    	choices = ANSWER, required = True,
    	label = 'Se necesita de un cuidado de temperatura?',
    	widget = forms.Select(attrs={'class': 'form-control'})
    )
    class Meta:
        model = ProductRequest
        fields = ['title', 'description', 'quantity', 'requested_date', 'temperature_care']