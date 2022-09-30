from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


from django.core.validators import MinValueValidator, MaxValueValidator


from django.db import models


USER_TYPE = (
    ('PRODUCTOR', 'PRODUCTOR'),
    ('CONSULTOR', 'CONSULTOR'),
    ('CLIENTE EXTERNO', 'CLIENTE EXTERNO'),
    ('CLIENTE INTERNO', 'CLIENTE INTERNO'),
    ('TRANSPORTISTA', 'TRANSPORTISTA'),
)

OFFER_STATUS = (
	('PENDIENTE', 'PENDIENTE'),
	('APROBADO', 'APROBADO'),
	('RECHAZADO', 'REFHAZADO'),
)


TYPE_BANK_ACCOUNT = (
	('CUENTA CORRIENTE', 'CUENTA CORRIENTE'),
	('CUENTA AHORRO', 'CUENTA AHORRO'),
	('CUENTA VISTA', 'CUENTA VISTA'),
	('CUENTA RUT', 'CUENTA RUT'),
	('CHEQUERA ELECTRONICA', 'CHEQUERA ELECTRONICA'),
)

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

CONTRACT_STATUS = (
    ('EN PROCESO', 'EN PROCESO'),
    ('FINALIZADO', 'FINALIZADO'),
)

ANSWER = (
	('SI', 'SI'),
	('NO', 'NO'),
)



class CustomUser(AbstractUser):
	type = models.CharField(max_length = 15, choices = USER_TYPE, default = '')



class Profile(models.Model):
	user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
	image = models.ImageField(default='user.png')
	
    
	def __str__(self):
		return f'Perfil de {self.user.username}'

	def following(self):
		user_ids = Relationship.objects.filter(from_user=self.user).values_list('to_user_id', flat=True)
		return CustomUser.objects.filter(id__in=user_ids)

	def followers(self):
		user_ids = Relationship.objects.filter(to_user=self.user).values_list('from_user_id', flat=True)
		return CustomUser.objects.filter(id__in=user_ids)


		


class Post(models.Model):
	timestamp = models.DateTimeField(default=timezone.now)
	user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='posts')
	title = models.CharField(max_length=300, blank = True)
	description = models.TextField(max_length=1000, blank = True)
	price = models.IntegerField(validators = [MinValueValidator(1000), MaxValueValidator(1000000000)])
	quantity = models.IntegerField(validators = [MinValueValidator(1), MaxValueValidator(1000)])
	image = models.ImageField(upload_to='media/post/', null=True)

	class Meta:
		ordering = ['-timestamp', 'price']

	def __str__(self):
		return f'{self.user.username} : {self.title}'


class Relationship(models.Model):
	from_user = models.ForeignKey(CustomUser, related_name='relationships', on_delete=models.CASCADE)
	to_user = models.ForeignKey(CustomUser, related_name='related_to', on_delete=models.CASCADE)

	def __str__(self):
		return f'{self.from_user} to {self.to_user}'

	class Meta:
		indexes = [
			models.Index(fields=['from_user', 'to_user',]),
		]

class Contact(models.Model):
    id_request = models.AutoField(primary_key=True, editable=False)
    first_name = models.CharField(max_length=60, blank = True)
    last_name = models.CharField(max_length=60, blank = True)
    
    email = models.EmailField(max_length=50, blank = True)
    subject = models.CharField(max_length=300, blank = True)
    text = models.TextField(max_length=1000, blank = True)
    timestamp = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f'Solicitud #{self.id_request} - {self.first_name} {self.last_name} : {self.subject}'


class Contract(models.Model):
	id_contract = models.AutoField(primary_key = True, editable = False)
	image = models.ImageField(upload_to='media/contract/', null = True)
	rut = models.CharField(max_length = 12, blank = True)
	phono = models.IntegerField(validators = [MinValueValidator(10000000000), MaxValueValidator(99999999999)])
	issued_date = models.DateTimeField(default = timezone.now)
	status = models.CharField(max_length = 10, blank = True)
	contract_closing_date = models.DateTimeField()

	class Meta:
		ordering = ['-issued_date', 'status']

	def __str__(self):
		return f'Contrato #{self.id_contract}'


class BankAccount(models.Model):
	id_bank_account = models.AutoField(primary_key = True, editable = False)
	user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name = 'bank')
	bank_name = models.CharField(max_length = 50, choices = BANK_NAMES, default = '')
	type_bank_account = models.CharField(max_length = 25, choices = TYPE_BANK_ACCOUNT, default = '')
	bank_account_number = models.IntegerField(validators = [MinValueValidator(10000000), MaxValueValidator(999999999999)])
	owner_full_name = models.CharField(max_length = 100, blank = True)


	class Meta:
		ordering = ['bank_name']

	def __str__(self):
		return f'{self.bank_name} - {self.type_bank_account}'


class ProductRequest(models.Model):
	id_product_request = models.AutoField(primary_key = True, editable = False)
	timestamp = models.DateTimeField(default=timezone.now)
	user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='product_request')
	title = models.CharField(max_length=300, blank = True)
	description = models.TextField(max_length=1000, blank = True)
	quantity = models.IntegerField(validators = [MinValueValidator(1), MaxValueValidator(1000)])
	requested_date = models.DateTimeField()
	temperature_care = models.CharField(max_length = 2, blank = True)

	class Meta:
		ordering = ['-timestamp']

	def __str__(self):
		return f'Solicitud de producto #{self.user.username} : {self.title}'

class ProductRequestStatus(models.Model):
	timestamp = models.DateTimeField(default=timezone.now)
	id_offered_product = models.IntegerField(validators = [MinValueValidator(1), MaxValueValidator(10000000000)])
	offer = models.CharField(max_length=300, blank = True)
	status = models.CharField(max_length = 20, choices = OFFER_STATUS, default = 'PENDIENTE')


	class Meta:
		ordering = ['-timestamp']

	def __str__(self):
		return f'Estado de la solicitud del producto #{self.id_offered_product} : {self.status}'