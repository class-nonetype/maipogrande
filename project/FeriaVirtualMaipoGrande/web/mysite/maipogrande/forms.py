
from .models import (
    Contact,
    CustomUser,
    Product,
    Contract,
    BankAccount,
    ProductRequest,
    Transport,

    USER_TYPE, TYPE_BANK_ACCOUNT, TYPE_TRANSPORT,
    BANK_NAMES, CONTRACT_STATUS, ANSWER, COUNTRY
)

from django.core.validators import MinValueValidator, MaxValueValidator
from django import forms
from django.contrib.auth.forms import UserCreationForm

import datetime


###################################################################
#   Formulario de registro de usuario                             #
###################################################################
class SignUpForm(UserCreationForm):
    
    first_name = forms.CharField(
        label = 'Nombres',
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control text-uppercase',
                'id' : 'input-first-name',
                'placeholder' : 'Ingresa tus nombres'
            }
        )
    )

    last_name = forms.CharField(
        label = 'Apellidos',
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control  text-uppercase',
                'id' : 'input-last-name',
                'placeholder' : 'Ingresa tus apellidos'
            }
        )
    )

    email = forms.EmailField(
        label = 'E-mail',
        widget = forms.EmailInput(
            attrs = {
                'class': 'form-control',
                'id' : 'input-email',
                'placeholder' : 'Ingresa tu e-mail'
            }
        )
    )

    username = forms.CharField(
        label = 'Nombre de Usuario',
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control',
                'id' : 'input-username',
                'placeholder' : 'Ingresa el nombre de usuario de la cuenta a crear'
            }
        )
    )


    password1 = forms.CharField(
        label = 'Contraseña',
        widget = forms.PasswordInput(
            attrs = {
                'class': 'form-control',
                'id' : 'input-password1',
                'placeholder' : 'Ingresa la contraseña de la cuenta a crear'
            }
        )
    )


    password2 = forms.CharField(
        label = 'Confirma la contraseña',
        widget = forms.PasswordInput(
            attrs = {
                'class': 'form-control',
                'id' : 'input-password2',
                'placeholder' : 'Confirma la contraseña'
            }
        )
    )


    type = forms.ChoiceField(
    	choices=USER_TYPE,
        required = True,
    	label = 'Selecciona el tipo de usuario a crear',
    	widget = forms.Select(
            attrs = {
                'class': 'form-control',
                'id' : 'select-type-user'
            }
        )
    )
    country = forms.ChoiceField(
    	choices = COUNTRY,
        required = True,
    	label = 'Selecciona el pais de origen',
    	widget = forms.Select(
            attrs = {
                'class': 'form-control',
                'id' : 'select-country',
            }
        )
    )

    identity_document_number = forms.IntegerField(
        required = True,
        label = 'Numero de documento de identidad',
        widget = forms.NumberInput(
            attrs = {
                'class': 'form-control',
                'id' : 'input-identity-document-number',
                'type':'number',
                'placeholder' : 'Ingresa tu numero de documento de identidad'
            }
        )
    )

    class Meta:

        model = CustomUser
        fields = UserCreationForm.Meta.fields + (
            'type', 'email', 'username', 'password1', 'password2',
            'identity_document_number', 'country', 'first_name', 'last_name',
        )
    
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
    
    def clean_first_name(self):
        return self.cleaned_data['first_name'].upper()
    
    def clean_last_name(self):
        return self.cleaned_data['last_name'].upper()





###################################################################
#   Formulario de publicacion del producto                        #
###################################################################
class ProductForm(forms.ModelForm):


    owner_full_name = forms.CharField(
        label = 'Nombre completo del titular',
        required = True,
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control',
                'id' : 'owner-full-name',
                'rows':2,
                'placeholder': 'Ingresa el nombre completo del titular'
            }
        )
    )

    title = forms.CharField(
        label = 'Titulo',
        required = True,
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control',
                'id' : 'product-title',
                'rows' : 2,
                'placeholder': 'Ej: Manzana'
            }
        )
    )

    description = forms.CharField(
        label = 'Descripcion',
        required = True,
        widget = forms.Textarea(
            attrs = {
                'class': 'form-control',
                'id' : 'product-description',
                'rows' : 2,
                'placeholder': 'Agrega una descripcion'
            }
        )
    )

    price = forms.IntegerField(
        label = 'Precio (kg)',
        required = True,
        widget = forms.NumberInput(
            attrs = {
                'class': 'form-control',
                'id' : 'product-price',
                'type':'number'
            }
        ),
        min_value = 100, max_value = 1000000000
    )
    
    quantity = forms.IntegerField(
        label = 'Cantidad (kg)',
        required = True,
        widget = forms.NumberInput(
            attrs = {
                'class': 'form-control',
                'id' : 'product-quantity',
                'type':'number'
            }
        ),
        min_value = 1, max_value = 10000
    )
    
    image = forms.ImageField(
        label = 'Selecciona la imagen',
        widget = forms.FileInput(
            attrs = {
                'class': 'form-control',
                'id' : 'product-img'
            }
        )
    )
    
    class Meta:
        
        model = Product
        fields = ['title', 'price', 'quantity', 'description', 'image']





###################################################################
#   Formulario de contacto                                        #
###################################################################
class ContactForm(forms.ModelForm):
    first_name = forms.CharField(
        label = 'Nombres',
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control'
            }
        )
    )

    last_name = forms.CharField(
        label = 'Apellidos',
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control'
            }
        )
    )

    email = forms.EmailField(
        label = 'E-mail',
        widget = forms.EmailInput(
            attrs = {
                'class': 'form-control'
            }
        )
    )

    subject = forms.CharField(
        label = 'Asunto',
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control'
            }
        )
    )

    text = forms.CharField(
        label = 'Descripcion',
        widget = forms.Textarea(
            attrs = {
                'class': 'form-control'
            }
        )
    )

    
    class Meta:
        
        model = Contact
        
        fields = [
            'first_name', 'last_name', 'email', 'subject', 'text', 
        ]





###################################################################
#   Formulario de contrato                                        #
###################################################################
class ContractForm(forms.ModelForm):

    document = forms.FileField(
        label = 'Selecciona la imagen',
        widget = forms.FileInput(
            attrs = {
                'class': 'form-control'
            }
        )
    )

    rut = forms.CharField(
        label = 'Rut',
        required = True,
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control',
                'rows' : 2,
                'placeholder': 'Ej: 11.111.111-1'
            }
        )
    )

    phono = forms.IntegerField(
        label = 'Numero de contacto',
        required = True,
        widget = forms.NumberInput(
            attrs = {
                'class': 'form-control',
                'type':'number'
            }
        )
    )

    issued_date = forms.DateTimeField(
        input_formats = ['%d/%m/%Y %H:%M:%S'],
        widget = forms.DateTimeInput(
            format='%d/%m/%Y %H:%M:%S',
            attrs = {
                'class': 'form-control'
            }
        )
    )
    
    contract_closing_date = forms.DateTimeField(
        input_formats = ['%d/%m/%Y %H:%M:%S'],
        widget = forms.DateTimeInput(
            format = '%d/%m/%Y %H:%M:%S',
            attrs = {
                'class': 'form-control'
            }
        )
    )
    
    status = forms.ChoiceField(
    	choices = CONTRACT_STATUS,
        required = True,
    	label = 'Selecciona el estado del contrato',
    	widget = forms.Select(
            attrs = {
                'class': 'form-control'
            }
        )
    )

    class Meta:
        model = Contract
        fields = ['image', 'rut', 'phono', 'issued_date', 'contract_closing_date']





###################################################################
#   Formulario de cuenta bancaria                                 #
###################################################################
class BankAccountForm(forms.ModelForm):
    bank_name = forms.ChoiceField(
        choices = BANK_NAMES,
        required = True,
        label = 'Selecciona el nombre del banco',
        widget = forms.Select(
            attrs = {
                'class': 'form-control',
                'id' : 'bank-name'
            }
        )
    )

    type_bank_account = forms.ChoiceField(
        choices = TYPE_BANK_ACCOUNT,
        required = True,
        label = 'Selecciona el tipo de cuenta',
        widget = forms.Select(
            attrs = {
                'class': 'form-control',
                'id' : 'bank-type'
            }
        )
    )
    bank_account_number = forms.IntegerField(
        label = 'Numero de Cuenta',
        required = True,
        widget = forms.NumberInput(
            attrs = {
                'class': 'form-control',
                'type':'number',
                'placeholder' : 'Ej : 11222333', 'id' : 'bank-account-number'
            }
        )
    )

    owner_full_name = forms.CharField(
        label = 'Nombre completo del titular',
        required = True,
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control',
                'rows' : 2,
                'placeholder': 'Ingresa el nombre completo del titular',
                'id' : 'bank-owner-full-name'
            }
        )
    )
    
    class Meta:
        model = BankAccount
        fields = ['bank_name', 'type_bank_account', 'bank_account_number', 'owner_full_name']





###################################################################
#   Formulario de solicitud del producto                          #
###################################################################
class ProductRequestForm(forms.ModelForm):

    title = forms.CharField(
        label = 'Titulo',
        required = True,
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control',
                'rows' : 2,
                'placeholder': 'Ej: Manzana'
            }
        )
    )

    description = forms.CharField(
        label = 'Descripcion',
        required = True,
        widget = forms.Textarea(
            attrs = {
                'class': 'form-control',
                'rows' : 2,
                'placeholder': 'Agrega una descripcion'
            }
        )
    )
    quantity = forms.IntegerField(
        label = 'Cantidad (kg)',
        widget = forms.NumberInput(
            attrs = {
                'class': 'form-control',
                'type':'number'
            }
        ),
        min_value = 1, max_value = 1000
    )

    requested_date = forms.DateField(
        label = 'Fecha solicitada',
        input_formats = ['%d/%m/%Y'],
        initial = datetime.date.today(),
        widget = forms.SelectDateWidget(
            attrs = {
                'class': 'form-control snps-inline-select'
            }
        )
    )

    temperature_care = forms.ChoiceField(
    	choices = ANSWER,
        required = True,
    	label = 'Se necesita de un cuidado de temperatura?',
    	widget = forms.Select(
            attrs = {
                'class': 'form-control'
            }
        )
    )

    delivery_place_city = forms.CharField(
        label = 'Ciudad del lugar de entrega',
        required = True,
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control',
                'rows' : 2,
                'placeholder': 'Agrega una ciudad para la entrega del producto'
            }
        )
    )

    delivery_place_address = forms.CharField(
        label = 'Direccion del lugar de entrega',
        required = True,
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control',
                'rows' : 2,
                'placeholder': 'Agrega una direccion para la entrega del producto'
            }
        )
    )

    delivery_address_number = forms.IntegerField(
        label = 'Numero de direccion/calle del lugar de entrega',
        widget = forms.NumberInput(
            attrs = {
                'class': 'form-control',
                'type':'number'
            }
        ),
        min_value = 1,  max_value=999999
    )
    
    class Meta:
        model = ProductRequest
        fields = [
            'title', 'description', 'quantity', 'requested_date', 'temperature_care',
            'delivery_place_city', 'delivery_place_address', 'delivery_address_number'
        ]





###################################################################
#   Formulario del estado de solicitud del producto               #
###################################################################
class ProductRequestStatusForm(forms.ModelForm):

    offer = forms.CharField(
        label = 'Producto ofrecido',
        required = True,
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control',
                'rows' : 2,
                'placeholder': 'Ej: Manzana'
            }
        )
    )
    
    description = forms.CharField(
        label = 'Descripcion',
        required = True,
        widget = forms.Textarea(
            attrs = {
                'class': 'form-control',
                'rows' : 2,
                'placeholder': 'Agrega una descripcion'
            }
        )
    )

    quantity = forms.IntegerField(
        label = 'Cantidad (kg)',
        widget = forms.NumberInput(
            attrs = {
                'class': 'form-control',
                'type':'number'
            }
        ),
        min_value = 1, max_value = 1000
    )
    requested_date = forms.DateField(
        label = 'Fecha solicitada',
        input_formats = ['%d/%m/%Y'],
        initial = datetime.date.today(),
        widget = forms.SelectDateWidget(
            attrs = {
                'class': 'form-control snps-inline-select'
            }
        )
    )
    temperature_care = forms.ChoiceField(
    	choices = ANSWER,
        required = True,
    	label = 'Se necesita de un cuidado de temperatura?',
    	widget = forms.Select(
            attrs = {
                'class': 'form-control'
            }
        )
    )

    class Meta:
        model = ProductRequest
        fields = [
            'title', 'description', 'quantity', 'requested_date', 'temperature_care'
        ]





###################################################################
#   Formulario de publicacion de transporte                       #
###################################################################
class TransportForm(forms.ModelForm):
    
    type = forms.ChoiceField(
        choices = TYPE_TRANSPORT,
        required = True,
        label = 'Selecciona el tipo de transporte',
        widget = forms.Select(
            attrs = {
                'class': 'form-control'
            }
        )
    )
    
    patent = forms.CharField(
        label = 'Patente del transporte',
        required = True,
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control',
                'rows' : 2,
                'placeholder': 'Ej: RX-GH-35'
            }
        )
    )
    
    size = forms.CharField(
        label = 'Tamaño',
        required = True,
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control',
                'rows' : 2,
                'placeholder': 'Ej: 16.50m x 4.30m'
            }
        )
    )
    
    capacity = forms.IntegerField(
        label = 'Capacidad de soporte (kg)', 
        widget = forms.NumberInput(
            attrs = {
                'class': 'form-control',
                'type':'number'
            }
        ),
        min_value = 1, max_value = 5000
    )
    
    image = forms.ImageField(
        label = 'Selecciona la imagen',
        widget = forms.FileInput(
            attrs = {
                'class': 'form-control'
            }
        )
    )
    
    refrigeration = forms.ChoiceField(
        choices = ANSWER,
        required = True,
        label = '¿Cuenta con refrigeracion?',
        widget = forms.Select(
            attrs = {
                'class': 'form-control'
            }
        )
    )
    
    
    class Meta:
        model = Transport
        fields = ['type', 'patent', 'size', 'capacity', 'image', 'refrigeration']
