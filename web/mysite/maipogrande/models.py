from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.validators import RegexValidator
from django.utils.text import gettext_lazy as _

###################################################################
#   Roles de usuario                                              #
###################################################################

USER_TYPE = (
    ('PRODUCTOR', 'PRODUCTOR'),
    ('CONSULTOR', 'CONSULTOR'),
    ('CLIENTE EXTERNO', 'CLIENTE EXTERNO'),
    ('CLIENTE INTERNO', 'CLIENTE INTERNO'),
    ('TRANSPORTISTA', 'TRANSPORTISTA'),
)


###################################################################
#   Estados de ventas                                             #
###################################################################
TYPE_SALE = (
    ('NACIONAL', 'NACIONAL'),
    ('INTERNACIONAL', 'INTERNACIONAL'),
)

###################################################################
#   Estados de ofertas                                            #
###################################################################

OFFER_STATUS = (
	('PENDIENTE', 'PENDIENTE'),
	('APROBADO', 'APROBADO'),
	('RECHAZADO', 'REFHAZADO'),
)

TRACKING_STATUS = (
    ('PEDIDO AUN NO PROCESADO', 'PEDIDO AUN NO PROCESADO'),
    ('PEDIDO PROCESADO', 'PEDIDO PROCESADO'),
    ('EN TRANSITO', 'EN TRANSITO'),
    ('PEDIDO ENTREGADO', 'PEDIDO ENTREGADO')
)

###################################################################
#   Tipos de transporte                                           #
###################################################################

TYPE_TRANSPORT = (
    ('CAMION', 'CAMION'),
    ('CAMIONETA', 'CAMIONETA'),
    ('AUTO', 'AUTO'),
    ('AVION', 'AVION'),
    ('AVIONETA', 'AVIONETA'),
    ('HELICOPTERO', 'HELICOPTERO'),
    ('BARCO', 'BARCO'),
    ('LANCHA', 'LANCHA'),

)

###################################################################
#   Tipos de cuentas bancarias                                    #
###################################################################

TYPE_BANK_ACCOUNT = (
	('CUENTA CORRIENTE', 'CUENTA CORRIENTE'),
	('CUENTA AHORRO', 'CUENTA AHORRO'),
	('CUENTA VISTA', 'CUENTA VISTA'),
	('CUENTA RUT', 'CUENTA RUT'),
	('CHEQUERA ELECTRONICA', 'CHEQUERA ELECTRONICA'),
)

###################################################################
#   Nombre de bancos                                              #
###################################################################

BANK_NAMES = (
    ('BANCO ESTADO', 'BANCO ESTADO'),
    ('MERCADO PAGO', 'MERCADO PAGO'),
    ('TAPP CAJA LOS ANDES', 'TAPP CAJA LOS ANDES'),
    ('PREPAGO TENPO', 'PREPAGO TENPO'),
    ('PREPAGO LOS HEROES', 'PREPAGO LOS HEROES'),
    ('COOPEUCH', 'COOPEUCH'),
    ('BANCO BBVA', 'BANCO BBVA'),
    ('BANCO CONSORCIO', 'BANCO CONSORCIO'),
    ('BANCO RIPLEY', 'BANCO RIPLEY'),
    ('BANCO FALABELLA', 'BANCO FALABELLA'),
    ('BANCO SECURITY', 'BANCO SECURITY'),
	('THE BANK OF TOKYO MITSUBISHI UFJ', 'THE BANK OF TOKYO MITSUBISHI UFJ'),
	('BANCO ITAU', 'BANCO ITAU'),
    ('BANCO SANTANDER', 'BANCO SANTANDER'),
    ('HSBC BANK CHILE', 'HSBC BANK CHILE'),
    ('BICE', 'BICE'),
    ('CORP BANCA', 'CORP BANCA'),
    ('BANCO DE CREDITO E INVERSIONES', 'BANCO DE CREDITO E INVERSIONES'),
    ('SCOTIABANK DESARROLLO', 'SCOTIABANK DESARROLLO'),
    ('BANCO INTERNACIONAL', 'BANCO INTERNACIONAL'),
    ('BANCO DE CHILE', 'BANCO DE CHILE'),
)

###################################################################
#   Estados de contrato                                           #
###################################################################
CONTRACT_STATUS = (
    ('EN PROCESO', 'EN PROCESO'),
    ('FINALIZADO', 'FINALIZADO'),
)

###################################################################
#   Respuestas                                                    #
###################################################################
ANSWER = (
	('NO', 'NO'),
	('SI', 'SI'),
)

###################################################################
#   Nombre de paises                                              #
###################################################################
COUNTRY = [
    ('US', 'United States'),
    ('AF', 'Afghanistan'),
    ('AL', 'Albania'),
    ('DZ', 'Algeria'),
    ('AS', 'American Samoa'),
    ('AD', 'Andorra'),
    ('AO', 'Angola'),
    ('AI', 'Anguilla'),
    ('AQ', 'Antarctica'),
    ('AG', 'Antigua And Barbuda'),
    ('AR', 'Argentina'),
    ('AM', 'Armenia'),
    ('AW', 'Aruba'),
    ('AU', 'Australia'),
    ('AT', 'Austria'),
    ('AZ', 'Azerbaijan'),
    ('BS', 'Bahamas'),
    ('BH', 'Bahrain'),
    ('BD', 'Bangladesh'),
    ('BB', 'Barbados'),
    ('BY', 'Belarus'),
    ('BE', 'Belgium'),
    ('BZ', 'Belize'),
    ('BJ', 'Benin'),
    ('BM', 'Bermuda'),
    ('BT', 'Bhutan'),
    ('BO', 'Bolivia'),
    ('BA', 'Bosnia And Herzegowina'),
    ('BW', 'Botswana'),
    ('BV', 'Bouvet Island'),
    ('BR', 'Brazil'),
    ('BN', 'Brunei Darussalam'),
    ('BG', 'Bulgaria'),
    ('BF', 'Burkina Faso'),
    ('BI', 'Burundi'),
    ('KH', 'Cambodia'),
    ('CM', 'Cameroon'),
    ('CA', 'Canada'),
    ('CV', 'Cape Verde'),
    ('KY', 'Cayman Islands'),
    ('CF', 'Central African Rep'),
    ('TD', 'Chad'),
    ('CL', 'Chile'),
    ('CN', 'China'),
    ('CX', 'Christmas Island'),
    ('CC', 'Cocos Islands'),
    ('CO', 'Colombia'),
    ('KM', 'Comoros'),
    ('CG', 'Congo'),
    ('CK', 'Cook Islands'),
    ('CR', 'Costa Rica'),
    ('CI', 'Cote D`ivoire'),
    ('HR', 'Croatia'),
    ('CU', 'Cuba'),
    ('CY', 'Cyprus'),
    ('CZ', 'Czech Republic'),
    ('DK', 'Denmark'),
    ('DJ', 'Djibouti'),
    ('DM', 'Dominica'),
    ('DO', 'Dominican Republic'),
    ('TP', 'East Timor'),
    ('EC', 'Ecuador'),
    ('EG', 'Egypt'),
    ('SV', 'El Salvador'),
    ('GQ', 'Equatorial Guinea'),
    ('ER', 'Eritrea'),
    ('EE', 'Estonia'),
    ('ET', 'Ethiopia'),
    ('FK', 'Falkland Islands (Malvinas)'),
    ('FO', 'Faroe Islands'),
    ('FJ', 'Fiji'),
    ('FI', 'Finland'),
    ('FR', 'France'),
    ('GF', 'French Guiana'),
    ('PF', 'French Polynesia'),
    ('TF', 'French S. Territories'),
    ('GA', 'Gabon'),
    ('GM', 'Gambia'),
    ('GE', 'Georgia'),
    ('DE', 'Germany'),
    ('GH', 'Ghana'),
    ('GI', 'Gibraltar'),
    ('GR', 'Greece'),
    ('GL', 'Greenland'),
    ('GD', 'Grenada'),
    ('GP', 'Guadeloupe'),
    ('GU', 'Guam'),
    ('GT', 'Guatemala'),
    ('GN', 'Guinea'),
    ('GW', 'Guinea-bissau'),
    ('GY', 'Guyana'),
    ('HT', 'Haiti'),
    ('HN', 'Honduras'),
    ('HK', 'Hong Kong'),
    ('HU', 'Hungary'),
    ('IS', 'Iceland'),
    ('IN', 'India'),
    ('ID', 'Indonesia'),
    ('IR', 'Iran'),
    ('IQ', 'Iraq'),
    ('IE', 'Ireland'),
    ('IL', 'Israel'),
    ('IT', 'Italy'),
    ('JM', 'Jamaica'),
    ('JP', 'Japan'),
    ('JO', 'Jordan'),
    ('KZ', 'Kazakhstan'),
    ('KE', 'Kenya'),
    ('KI', 'Kiribati'),
    ('KP', 'Korea (North)'),
    ('KR', 'Korea (South)'),
    ('KW', 'Kuwait'),
    ('KG', 'Kyrgyzstan'),
    ('LA', 'Laos'),
    ('LV', 'Latvia'),
    ('LB', 'Lebanon'),
    ('LS', 'Lesotho'),
    ('LR', 'Liberia'),
    ('LY', 'Libya'),
    ('LI', 'Liechtenstein'),
    ('LT', 'Lithuania'),
    ('LU', 'Luxembourg'),
    ('MO', 'Macau'),
    ('MK', 'Macedonia'),
    ('MG', 'Madagascar'),
    ('MW', 'Malawi'),
    ('MY', 'Malaysia'),
    ('MV', 'Maldives'),
    ('ML', 'Mali'),
    ('MT', 'Malta'),
    ('MH', 'Marshall Islands'),
    ('MQ', 'Martinique'),
    ('MR', 'Mauritania'),
    ('MU', 'Mauritius'),
    ('YT', 'Mayotte'),
    ('MX', 'Mexico'),
    ('FM', 'Micronesia'),
    ('MD', 'Moldova'),
    ('MC', 'Monaco'),
    ('MN', 'Mongolia'),
    ('MS', 'Montserrat'),
    ('MA', 'Morocco'),
    ('MZ', 'Mozambique'),
    ('MM', 'Myanmar'),
    ('NA', 'Namibia'),
    ('NR', 'Nauru'),
    ('NP', 'Nepal'),
    ('NL', 'Netherlands'),
    ('AN', 'Netherlands Antilles'),
    ('NC', 'New Caledonia'),
    ('NZ', 'New Zealand'),
    ('NI', 'Nicaragua'),
    ('NE', 'Niger'),
    ('NG', 'Nigeria'),
    ('NU', 'Niue'),
    ('NF', 'Norfolk Island'),
    ('MP', 'Northern Mariana Islands'),
    ('NO', 'Norway'),
    ('OM', 'Oman'),
    ('PK', 'Pakistan'),
    ('PW', 'Palau'),
    ('PA', 'Panama'),
    ('PG', 'Papua New Guinea'),
    ('PY', 'Paraguay'),
    ('PE', 'Peru'),
    ('PH', 'Philippines'),
    ('PN', 'Pitcairn'),
    ('PL', 'Poland'),
    ('PT', 'Portugal'),
    ('PR', 'Puerto Rico'),
    ('QA', 'Qatar'),
    ('RE', 'Reunion'),
    ('RO', 'Romania'),
    ('RU', 'Russian Federation'),
    ('RW', 'Rwanda'),
    ('KN', 'Saint Kitts And Nevis'),
    ('LC', 'Saint Lucia'),
    ('VC', 'St Vincent/Grenadines'),
    ('WS', 'Samoa'),
    ('SM', 'San Marino'),
    ('ST', 'Sao Tome'),
    ('SA', 'Saudi Arabia'),
    ('SN', 'Senegal'),
    ('SC', 'Seychelles'),
    ('SL', 'Sierra Leone'),
    ('SG', 'Singapore'),
    ('SK', 'Slovakia'),
    ('SI', 'Slovenia'),
    ('SB', 'Solomon Islands'),
    ('SO', 'Somalia'),
    ('ZA', 'South Africa'),
    ('ES', 'Spain'),
    ('LK', 'Sri Lanka'),
    ('SH', 'St. Helena'),
    ('PM', 'St.Pierre'),
    ('SD', 'Sudan'),
    ('SR', 'Suriname'),
    ('SZ', 'Swaziland'),
    ('SE', 'Sweden'),
    ('CH', 'Switzerland'),
    ('SY', 'Syrian Arab Republic'),
    ('TW', 'Taiwan'),
    ('TJ', 'Tajikistan'),
    ('TZ', 'Tanzania'),
    ('TH', 'Thailand'),
    ('TG', 'Togo'),
    ('TK', 'Tokelau'),
    ('TO', 'Tonga'),
    ('TT', 'Trinidad And Tobago'),
    ('TN', 'Tunisia'),
    ('TR', 'Turkey'),
    ('TM', 'Turkmenistan'),
    ('TV', 'Tuvalu'),
    ('UG', 'Uganda'),
    ('UA', 'Ukraine'),
    ('AE', 'United Arab Emirates'),
    ('UK', 'United Kingdom'),
    ('UY', 'Uruguay'),
    ('UZ', 'Uzbekistan'),
    ('VU', 'Vanuatu'),
    ('VA', 'Vatican City State'),
    ('VE', 'Venezuela'),
    ('VN', 'Viet Nam'),
    ('VG', 'Virgin Islands (British)'),
    ('VI', 'Virgin Islands (U.S.)'),
    ('EH', 'Western Sahara'),
    ('YE', 'Yemen'),
    ('YU', 'Yugoslavia'),
    ('ZR', 'Zaire'),
    ('ZM', 'Zambia'),
    ('ZW', 'Zimbabwe')
]



###################################################################
#   Clase del modelo de usuario                                   #
###################################################################
class CustomUser(AbstractUser):
    
    type = models.CharField(
        max_length = 15,
        choices = USER_TYPE,
        default = USER_TYPE[2][0]
    )

    identity_document_number = models.IntegerField(
        null=True,
        validators = [MinValueValidator(100000), MaxValueValidator(99999999999)]
    )

    country = models.CharField(
        max_length = 20,
        choices = COUNTRY,
        default = ''
    )





###################################################################
#   Clase del modelo de perfil de usuario                         #
###################################################################
class Profile(models.Model):

	user = models.OneToOneField(
        CustomUser,
        on_delete = models.CASCADE
    )
    
	image = models.ImageField(
        default = 'media/profile/user.ico'
    )
	
	def __str__(self):
		return f'Perfil de {self.user.username}'

	def following(self):
		user_ids = Relationship.objects.filter(from_user = self.user).values_list('to_user_id', flat = True)
		
		return CustomUser.objects.filter(id__in = user_ids)

	def followers(self):
		user_ids = Relationship.objects.filter(to_user = self.user).values_list('from_user_id', flat = True)
		
		return CustomUser.objects.filter(id__in = user_ids)





###################################################################
#   Clase del modelo de producto                                  #
###################################################################
class Product(models.Model):
    id = models.AutoField(
        primary_key = True,
        editable = False
    )
    
    timestamp = models.DateTimeField(
        default = timezone.localtime(timezone.now()).strftime("%Y-%m-%d %H:%M:%S")
    )
    
    user = models.ForeignKey(
        CustomUser,
        on_delete = models.CASCADE,
        related_name = 'product'
    )
    
    title = models.CharField(
        max_length = 300,
        blank = True
    )
    
    description = models.TextField(
        max_length = 5000,
        blank = True
    )
    
    price = models.IntegerField(
        validators = [MinValueValidator(100), MaxValueValidator(1000000000)]
    )
    
    quantity = models.IntegerField(
        validators = [MinValueValidator(1), MaxValueValidator(1000)]
    )

    type_sale = models.CharField(
        max_length = 15,
        choices = TYPE_SALE,
        default = TYPE_SALE[0][0]
    )

    quality = models.IntegerField(
        validators = [MinValueValidator(1), MaxValueValidator(5)]
    )
    
    image = models.ImageField(
        upload_to = 'media/post/product/',
        null = True
    )
    
    owner_full_name = models.CharField(
        max_length = 100,
        blank = True
    )
    
    def __str__(self):
        return f'Producto : {str(self.title).upper()}'

    class Meta:
        ordering = ['-timestamp', 'price']





###################################################################
#   Clase del modelo de relacion de usuarios                      #
###################################################################
class Relationship(models.Model):
    from_user = models.ForeignKey(
        CustomUser,
        related_name = 'relationships',
        on_delete = models.CASCADE
    )
    to_user = models.ForeignKey(
        CustomUser,
        related_name = 'related_to',
        on_delete = models.CASCADE
    )
    
    def __str__(self):
        return f'Interes : {str(self.from_user).upper()} - {str(self.to_user).upper()}'

    class Meta:
        indexes = [
            models.Index(fields=['from_user', 'to_user',]),
        ]





###################################################################
#   Clase del modelo de contracto                                 #
###################################################################
class Contact(models.Model):
    
    id_request = models.AutoField(
        primary_key = True,
        editable = False
    )
    
    first_name = models.CharField(
        max_length = 60,
        blank = True
    )

    last_name = models.CharField(
        max_length = 60,
        blank = True
    )
    
    email = models.EmailField(
        max_length = 50,
        blank = True
    )

    subject = models.CharField(
        max_length = 300,
        blank = True)

    text = models.TextField(
        max_length = 5000,
        blank = True
    )

    timestamp = models.DateTimeField(
        default = timezone.now
    )

    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f'Solicitud #{self.id_request} de {str(self.first_name).upper()} {str(self.last_name).upper()} : {str(self.subject).upper()}'





###################################################################
#   Clase del modelo de contrato                                  #
###################################################################
class Contract(models.Model):
    
    id_contract = models.AutoField(
        primary_key = True,
        editable = False
    )
    
    document = models.FileField(
        upload_to = 'media/contract/',
        null = True
    )


    class Meta:
        ordering = ['document']
    
    def __str__(self):
        return f'Contrato #{self.id_contract}'




class InternationalContract(models.Model):

    id = models.AutoField(
        primary_key = True,
        editable = False
    )

    contract_term = models.DateTimeField(
        default = timezone.localtime(timezone.now()).strftime("%Y-%m-%d %H:%M:%S")
    )

    contract_closing_date = models.DateTimeField(
    )


    contract_validity = models.CharField(
        max_length = 2,
        default = ANSWER[0][0],
        blank = True
    )
    


###################################################################
#   Clase del modelo de cuenta bancaria del usuario               #
###################################################################
class BankAccount(models.Model):
    
    id_bank_account = models.AutoField(
        primary_key = True,
        editable = False
    )
    
    timestamp = models.DateTimeField(
        default = timezone.now
    )
    
    user = models.ForeignKey(
        CustomUser,
        on_delete = models.CASCADE,
        related_name = 'bank'
    )
    
    bank_name = models.CharField(
        max_length = 50,
        choices = BANK_NAMES,
        default = ''
    )
    
    type_bank_account = models.CharField(
        max_length = 25,
        choices = TYPE_BANK_ACCOUNT,
        default = ''
    )
    
    bank_account_number = models.IntegerField(
        validators = [MinValueValidator(1000), MaxValueValidator(999999999999)]
    )
    
    bank_amount = models.IntegerField(
        validators = [MinValueValidator(0), MaxValueValidator(999999999)],
        default = 0
    )
    
    owner_full_name = models.CharField(
        max_length = 100,
        blank = True
    )
    
    class Meta:
        ordering = ['bank_name']
    
    def __str__(self):
        return f'Titular {self.owner_full_name} | Banco {str(self.bank_name).upper()} : {str(self.type_bank_account).upper()}'





###################################################################
#   Clase del modelo de solicitud de producto                     #
###################################################################
class ProductRequest(models.Model):
    id_product_request = models.AutoField(
        primary_key = True,
        editable = False
    )
    
    timestamp = models.DateTimeField(
        default = timezone.now
    )
    
    user = models.ForeignKey(
        CustomUser,
        on_delete = models.CASCADE,
        related_name = 'product_request'
    )
    
    title = models.CharField(
        max_length = 300,
        blank = True
    )
    
    description = models.TextField(
        max_length = 1000,
        blank = True
    )
    
    quantity = models.IntegerField(
        validators = [MinValueValidator(1), MaxValueValidator(1000)]
    )
    
    requested_date = models.DateTimeField()
    
    temperature_care = models.CharField(
        max_length = 2,
        blank = True,
        default = ANSWER[0][0]
    )
    
    delivery_place_city = models.CharField(
        max_length = 300,
        blank = True
    )
    
    delivery_place_address = models.CharField(
        max_length = 300,
        blank = True
    )
    
    delivery_address_number = models.IntegerField(
        validators = [MinValueValidator(1), MaxValueValidator(999999)]
    )


    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f'Solicitud de producto #{self.id_product_request} : {str(self.title).upper()}'





###################################################################
#   Clase del modelo del estado de solicitud del producto         #
###################################################################
class ProductRequestStatus(models.Model):

    id_product_request_status = models.AutoField(
        primary_key = True,
        editable = False
    )

    id_product_request = models.ForeignKey(
        ProductRequest,
        on_delete = models.CASCADE,
        related_name = 'product_request_status',
        blank = True,
        null = True
    )
    

    id_offered_product = models.IntegerField(
        validators = [MinValueValidator(1), MaxValueValidator(10000000000)]
    )
    
    id_client = models.IntegerField(
        validators = [MinValueValidator(1), MaxValueValidator(10000000000)]
    )
    
    id_producer = models.IntegerField(
        validators = [MinValueValidator(1), MaxValueValidator(10000000000)]
    )
    
    id_offered_transport = models.IntegerField(
        validators = [MinValueValidator(1), MaxValueValidator(10000000000)]
    )
    
    offered_product = models.CharField(
        max_length = 150,
        blank = True
    )
    
    timestamp = models.DateTimeField(default=timezone.now)
    
    offered_transport = models.CharField(
        max_length = 150,
        blank = True,
        default = ''
    )
    
    status = models.CharField(
        max_length = 20,
        choices = OFFER_STATUS,
        default = OFFER_STATUS[0][0]
    )


    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f'Estado de la solicitud del producto #{self.id_offered_product} : {str(self.status).upper()}'





###################################################################
#   Clase del modelo de transaccion de venta                      #
###################################################################
class Transaction(models.Model):

    id_transaction = models.AutoField(
        primary_key = True,
        editable = False
    )
    
    id_product = models.IntegerField(
        validators = [MinValueValidator(1), MaxValueValidator(10000000000)]
    )
    
    id_transport = models.IntegerField(
        validators = [MinValueValidator(1), MaxValueValidator(10000000000)]
    )

    timestamp = models.DateTimeField(
        default = timezone.localtime(timezone.now()).strftime("%Y-%m-%d %H:%M:%S")
    )

    product = models.CharField(
        max_length = 100,
        blank = True
    )

    type_sale = models.CharField(
        max_length = 15,
        choices = TYPE_SALE,
        default = TYPE_SALE[0][0]
    )

    quantity = models.IntegerField(
        validators = [MinValueValidator(1), MaxValueValidator(1000)]
    )

    producer = models.CharField(
        max_length = 100,
        blank = True
    )

    client = models.CharField(
        max_length = 100,
        blank = True
    )

    transportist = models.CharField(
        max_length = 100,
        blank = True
    )

    price = models.IntegerField(
        validators = [MinValueValidator(1000), MaxValueValidator(1000000000)]
    )

    total = models.IntegerField(
        validators = [MinValueValidator(1000), MaxValueValidator(1000000000)]
    )

    transport_status = models.CharField(
        max_length = 2,
        choices = ANSWER,
        blank = True,
        default = ANSWER[0][0]
    )

    transport_type = models.CharField(
        max_length = 150,
        choices = TYPE_TRANSPORT,
        blank = True
    )

    transport_patent = models.CharField(
        max_length = 20, 
        blank = True
    )

    transport_size = models.CharField(
        max_length = 50, 
        blank = True
    )

    transport_capacity = models.IntegerField(
        validators = [MinValueValidator(1), MaxValueValidator(10000)],
        default = 0
    )

    transport_refrigeration = models.CharField(
        max_length = 2,
        choices = ANSWER,
        blank = True,
        default = ANSWER[0][0]
    )

    status = models.CharField(
        max_length = 20,
        choices = OFFER_STATUS,
        default = OFFER_STATUS[0][0]
    )


    class Meta:
        ordering = ['timestamp']
    
    def __str__(self):  
        return f'Transaccion #{self.id_transaction}'





###################################################################
#   Clase del modelo de transporte                                #
###################################################################
class Transport(models.Model):

    timestamp = models.DateTimeField(
        default = timezone.localtime(timezone.now()).strftime("%Y-%m-%d %H:%M:%S")
    )

    user = models.ForeignKey(
        CustomUser,
        on_delete = models.CASCADE,
        related_name = 'transport'
    )

    image = models.ImageField(
        upload_to = 'media/post/transport/',
        null = True
    )
    
    type = models.CharField(
        max_length = 15,
        blank = True,
        choices = TYPE_TRANSPORT,
        default = TYPE_TRANSPORT[0][0]
    )

    patent = models.CharField(
        max_length = 20,
        blank = True
    )
    
    size = models.CharField(
        max_length = 50,
        blank = True
    )
    
    capacity = models.IntegerField(
        validators = [MinValueValidator(1), MaxValueValidator(1000)]
    )
    
    refrigeration = models.CharField(
        max_length = 2,
        choices = ANSWER,
        default = ANSWER[0][0]
    )


    class Meta:
        ordering = ['timestamp', 'type']
    
    def __str__(self):  
        return f'Transporte {str(self.type).upper()} #{self.patent} : {self.user.username}'





###################################################################
#   Clase del modelo de solicitud de transporte                   #
###################################################################
class TransportRequestStatus(models.Model):
    id_transaction = models.AutoField(
        primary_key = True,
        editable = False
    )

    id_product = models.IntegerField(
        validators = [MinValueValidator(1), MaxValueValidator(10000000000)]
    )

    id_transport = models.IntegerField(
        validators = [MinValueValidator(1), MaxValueValidator(10000000000)]
    )

    producer = models.CharField(
        max_length = 150,
        blank = True
    )

    client = models.CharField(
        max_length = 150,
        blank = True
    )

    transportist = models.CharField(
        max_length = 150,
        blank = True
    )

    status = models.CharField(
        max_length = 25,
        choices = TRACKING_STATUS,
        default = TRACKING_STATUS[0][0]
    )
    
    tracking_number = models.CharField(
        max_length = 8
    )







class RechargeTransaction(models.Model):
    id = models.AutoField(
        primary_key = True,
        editable = False
    )

    id_bank_account = models.IntegerField(
        validators = [MinValueValidator(1), MaxValueValidator(10000000000)]
    )

    timestamp = models.DateTimeField(
        default = timezone.now
    )
    
    user = models.ForeignKey(
        CustomUser,
        on_delete = models.CASCADE,
        related_name = 'recharge'
    )

    charge = models.IntegerField(
        validators = [MinValueValidator(1000), MaxValueValidator(1000000000)]
    )


    