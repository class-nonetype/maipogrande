from django.contrib.auth import authenticate, login
from django.contrib import messages

from django.shortcuts import render, redirect, get_object_or_404
import random
from .models import (
    CustomUser,
	ProductRequest,
	Profile,
	Relationship,
	Product,
	BankAccount,
	ProductRequestStatus,
	Transport,
	Transaction,
	TransportRequestStatus,
	RechargeTransaction,
	Contract,
	InternationalContract,

	ANSWER, TRACKING_STATUS
)
from .forms import (
    BankAccountForm,
	ContactForm,
	ProductRequestForm,
	SignUpForm,
	ProductForm, 
	TransportForm,
	InternationalContractForm,
	ContractForm
)

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings
from django.db import connection

import time


###################################################################
#	Vista principal												  #
###################################################################
def home(request):

	if request.method == 'POST':
	
		contact_form = ContactForm(request.POST)

		if contact_form.is_valid():
			contact_form.save()

			return redirect('home')
	else:

		contact_form = ContactForm()

	context = {
		'contact_form' : contact_form
	}

	return render(request, 'home.html', context)



###################################################################
#	Vista de inicio de sesion del usuario						  #
###################################################################
def login(request):
    return render(request, 'login.html')



###################################################################
#	Vista de perfil del usuario									  #
#	Recibe los argumentos	username							  #
###################################################################
@login_required
def profile(request, username = None):

	current_user = request.user

	# if username and username != current_user.username
	if username != current_user:

		user = CustomUser.objects.get(username = username)
		product_post = user.product.all()

	else:

		product_post = current_user.product.all()
		user = current_user
	
	if user.type == 'TRANSPORTISTA':
		context = {
			'user' : user,
			'product_post' : Transport.objects.filter(user = user.id).all()
		}

	else:

		if request.user.type == 'CLIENTE EXTERNO' or request.user.type == 'CLIENTE INTERNO':
			client_user_full_name = f'''{user.first_name} {user.last_name}''' 

			transaction = Transaction.objects.filter(client = client_user_full_name).all()
		

		elif request.user.type == 'PRODUCTOR':
			producer_user_full_name = f'''{user.first_name} {user.last_name}''' 

			transaction = Transaction.objects.filter(producer = producer_user_full_name).all()

		elif request.user.type == 'TRANSPORTISTA':
			transportist_user_full_name = f'''{user.first_name} {user.last_name}''' 

			transaction = Transaction.objects.filter(transportist = transportist_user_full_name).all()
		
		elif request.user.type == 'CONSULTOR':
			transaction = Transaction.objects.filter(status = 'APROBADO').all()

		context = {
			'user': user,
			'transaction' : transaction,
			'product_post' : product_post
		}

	return render(request, 'profile.html', context)



###################################################################
#	Vista de las publicaciones de los productos creados por		  #
# 	el usuario de tipo productor								  #
###################################################################
@login_required
def feed(request):

	product_post = Product.objects.all()
	#product_post = Product.objects.filter().all()

	try:
		international_contract = InternationalContract.objects.get()
		
	except InternationalContract.DoesNotExist:
		international_contract = InternationalContract.objects.filter().all()



	context = {
		'product_post': product_post,
		'international_contract' : international_contract
	}

	return render(request, 'feed.html', context)



@login_required
def international_contract_feed(request):

	international_contract = InternationalContract.objects.get()

	product_post = Product.objects.filter(
		Q(quality=5) |
		Q(quality=3) |
		Q(quality=4) 
		#Q(type_sale='INTERNACIONAL')
	).all()


	context = {
		'product_post': product_post,
		'international_contract' : international_contract
	}

	return render(request, 'international-contract-feed.html', context)



###################################################################
#	Vista de la publicacion de un producto						  #
###################################################################
@login_required
def publish_product_post(request):

	current_user = get_object_or_404(CustomUser, pk=request.user.pk)
	user = CustomUser.objects.get(username=current_user)

	if request.method == 'POST':

		product_post_form = ProductForm(request.POST, request.FILES)
		product_post_form.initial = {
			'owner_full_name' : f'''{user.first_name} {user.last_name}'''.upper()
		}
		
		if product_post_form.is_valid():

			product_post = product_post_form.save(commit=False)
			product_post.user = current_user
			product_post.save()

			###################################################################
			#	Mensaje hacia el usuario con el detalle de la publicacion     #
			###################################################################

			__message = str(
				f'''Hola {current_user.first_name.upper()} {current_user.last_name.upper()}'''
				'''\n\nGracias por tu oferta. Se ha publicado tu producto y ahora está en espera hasta que confirmemos que exista alguna respuesta.'''
				'''\nMientras tanto, aquí tienes un recordatorio de lo que has ofrecido:'''
				f'''\n\tProducto: {product_post_form.cleaned_data['title']} '''
				f'''\n\tDescripcion:{product_post_form.cleaned_data['description']}'''
				f'''\n\tCantidad:{product_post_form.cleaned_data['quantity']}'''
				'''\n\n¡Gracias por usar Feria Virtual Maipo Grande!'''
			)
			
			###################################################################
			#	Manejo de excepcion en caso de que hayan problemas con la     #
			#	seguridad de la cuenta google de maipo.grande.object          #
			#															      #
			#	en caso de haber un problema, usar este link:                 #
			#	https://myaccount.google.com/security?hl=es_419               #
			#																  #
			#	Dirigirse a "Acceso a Google"								  #
			#	Verificacion en 2 pasos      SI								  #
			#	Contraseñas de aplicaciones	 (como requisito deberia haber 1) #
			###################################################################
			try:

				send_mail(
					subject = f'''FERIA VIRTUAL MAIPO GRANDE - Producto {product_post_form.cleaned_data['title']} ofrecido''',
					message = __message,
					from_email = settings.EMAIL_HOST_USER,
					recipient_list = [current_user.email, ]
				)
			
			except Exception:
				pass

			return redirect('feed')

	else:

		product_post_form = ProductForm()

		try:
			owner_full_name = f'''{user.first_name} {user.last_name}'''.upper()
			product_post_form.initial = {
				'owner_full_name' : owner_full_name
			}
		
		except Exception:
			pass
	
	context = {
		'product_post_form' : product_post_form
	}
		
	return render(request, 'publish-product-post.html', context)



###################################################################
#	Vista de la venta de producto								  #
#	Recibe los argumentos	id_product							  #
###################################################################
@login_required
def product_sale(request, id_product = None):
	current_user = get_object_or_404(CustomUser, pk = request.user.pk)

	if current_user.type == 'CLIENTE EXTERNO' or current_user.type == 'CLIENTE INTERNO':

		if request.method == 'POST':

			user = CustomUser.objects.get(username = current_user)
			product_post = Product.objects.get(id = id_product)
			bank_account = BankAccount.objects.filter(user = user)

			context = {
				'request' : request,
				'product_post' : product_post,
				'bank_account' : bank_account,
				'user' : user
			}

			print(context)
			
			return render(request, 'product-sale.html', context)

		else:

			user = CustomUser.objects.get(username = current_user)
			product_post = Product.objects.get(id = id_product)
			bank_account = BankAccount.objects.filter(user = user)

			context = {
				'request' : request,
				'product_post' : product_post,
				'bank_account' : bank_account,
				'user' : user
			}

			return render(request, 'product-sale.html', context)
	else:
		pass



###################################################################
#	Vista de la venta efectuada									  #
#	Recibe los argumentos	id_bank_account						  #
#							amount								  #
#							id_product							  #
#							quantity							  #
#							id_producer							  #
#							id_client							  #
#							price								  #
#							type_sale							  #
###################################################################
@login_required
def generate_sales_transaction(
	request, id_bank_account = None, amount = None,
	id_product = None, quantity = None, id_producer = None,
	id_client = None, price = None,
	type_sale = None):

	time.sleep(2)

	current_user = get_object_or_404(CustomUser, pk = request.user.pk)
	user = CustomUser.objects.get(username = current_user)

	#	Transaccion

	if user.type == 'CLIENTE EXTERNO' or user.type == 'CLIENTE INTERNO':
		bank_account = BankAccount.objects.get(id_bank_account = id_bank_account)

	

		###################################################################
		#	Si el saldo de la cuenta bancaria es menor al monto 		  #
		#	se redirecciona un mensaje de saldo insuficiente			  #
		###################################################################
		if bank_account.bank_amount < amount or bank_account.bank_amount <= 0:
			messages.warning(request, message = 'MENSAJE_SALDO_INSUFICIENTE')

			return redirect(request.META.get('HTTP_REFERER'))

		
		else:

			if bank_account.bank_amount <= 0:
				bank_account.bank_amount = 0
			
			else:
				bank_account.bank_amount = bank_account.bank_amount - amount

			bank_account.save()




			###################################################################
			#	Se obtiene el producto a traves de la id que se recibe 		  #
			#	como parametro												  #
			#																  #
			# 	Se le resta la cantidad de stock que el cliente compro		  #
			###################################################################

			product_post = Product.objects.get(id = id_product)
			product_post.quantity -= quantity

			if product_post.quantity < 0:
				product_post.quantity = 0

			product_post.save()



			producer_user = Profile.objects.get(id = id_producer)
			producer_user_first_name = producer_user.user.first_name
			producer_user_last_name = producer_user.user.last_name
			producer_user_full_name = f'''{producer_user_first_name} {producer_user_last_name}'''.upper()

			client_user = Profile.objects.get(id = id_client)
			client_user_first_name = client_user.user.first_name
			client_user_last_name = client_user.user.last_name
			client_user_full_name = f'''{client_user_first_name} {client_user_last_name}'''


			print(f'ID PRODUCTOR 					{id_producer}')
			print(f'NOMBRE COMPLETO PRODUCTOR 		{producer_user_full_name}')
			print(f'ID CLIENTE						{id_client}')
			print(f'NOMBRE COMPLETO CLIENTE			{client_user_full_name}')


			###################################################################
			#	Se obtiene la primera cuenta bancaria existente del productor #
			#	y se le suma el monto total									  #
			###################################################################


			bank_account = BankAccount.objects.filter(user_id = id_producer).first()


			__service = int(amount * (15/100))
			amount -= __service

			bank_account.bank_amount += amount
			print(amount)
			print(bank_account.bank_amount)
			
			bank_account.save()


			###################################################################
			#	Se instancia la transaccion con los argumentos recibidos      #
			###################################################################
			
			transaction = Transaction(
				id_product = id_product,
				id_transport = 0,

				product = Product.objects.get(id = id_product).title,
				quantity = quantity,

				producer = producer_user_full_name,
				client = client_user_full_name,
				type_sale = type_sale,
				transportist = 'PENDIENTE',
				price = price,
				total = amount,
				status = 'PENDIENTE'
			)
			transaction.save()


		###################################################################
		#	Mensaje hacia el productor con los detalles de la transaccion #
		###################################################################
		__message = str(
			f'''Hola {producer_user_full_name}'''
			f'''\n\nEl usuario {str(f'{Profile.objects.get(id=id_client).user.username}')} con nombre {client_user_full_name}'''
			f'''Ha comprado tu producto {Product.objects.get(id=id_product).title} y ahora está en espera hasta que confirmemos que exista algun transportista que pueda.'''
			'''\nMientras tanto, aquí tienes un resumen de la venta realizada:'''

			f'''\n\tProducto {Product.objects.get(id=id_product).title}'''
			f'''\n\tCantidad {quantity}'''
			f'''\n\tTotal {amount}'''
			'''\n\n¡Gracias por usar Feria Virtual Maipo Grande!'''
		)

		###################################################################
		#	Manejo de excepcion en caso de que hayan problemas con la     #
		#	seguridad de la cuenta google de maipo.grande.object          #
		#															      #
		#	en caso de haber un problema, usar este link:                 #
		#	https://myaccount.google.com/security?hl=es_419               #
		#																  #
		#	Dirigirse a "Acceso a Google"								  #
		#	Verificacion en 2 pasos      SI								  #
		#	Contraseñas de aplicaciones	 (como requisito deberia haber 1) #
		###################################################################

		try:
			send_mail(
				subject = f'''FERIA VIRTUAL MAIPO GRANDE - Producto {Product.objects.get(id=id_product).title} vendido''',
				message = __message,
				from_email = settings.EMAIL_HOST_USER,
				recipient_list = [Profile.objects.get(id = id_producer).user.email, ]
			)
		
		except Exception as exc:
			print(exc)
			return redirect('feed')


		__message = str(
			f'''Hola {client_user_full_name}'''
			f'''\n\nSe ha procesado exitosamente tu compra del producto {Product.objects.get(id=id_product).title} y ahora está en espera hasta que confirmemos que exista algun transportista que este operativo.'''
			'''\nMientras tanto, aquí tienes un resumen de la compra realizada:'''

			f'''\n\tProducto {Product.objects.get(id = id_product).title}'''
			f'''\n\tCantidad {quantity}'''
			f'''\n\tTotal ${amount}'''
			'''\n\n¡Gracias por usar Feria Virtual Maipo Grande!'''
		)


		###################################################################
		#	Manejo de excepcion en caso de que hayan problemas con la     #
		#	seguridad de la cuenta google de maipo.grande.object          #
		#															      #
		#	en caso de haber un problema, usar este link:                 #
		#	https://myaccount.google.com/security?hl=es_419               #
		#																  #
		#	Dirigirse a "Acceso a Google"								  #
		#	Verificacion en 2 pasos      SI								  #
		#	Contraseñas de aplicaciones	 (como requisito deberia haber 1) #
		###################################################################

		try:
			send_mail(
				subject = f'''FERIA VIRTUAL MAIPO GRANDE - Producto {Product.objects.get(id = id_product).title} comprado''',
				message = __message,
				from_email = settings.EMAIL_HOST_USER,
				recipient_list = [Profile.objects.get(id = id_client).user.email, ]
			)
		
		except Exception as exc:
			print(exc)

			return redirect('feed')

		messages.success(request, message = 'MENSAJE_TRANSACCION_REALIZADA')

		return redirect(request.META.get('HTTP_REFERER'))



###################################################################
#	Vista de la publicacion de un transporte					  #
###################################################################
@login_required
def publish_transport_post(request):

	current_user = get_object_or_404(CustomUser, pk = request.user.pk)

	if request.method == 'POST':

		transport_post_form = TransportForm(request.POST, request.FILES)

		if transport_post_form.is_valid():

			transport_post = transport_post_form.save(commit = False)
			transport_post.user = current_user
			transport_post.save()

			messages.success(request, message = 'MENSAJE_TRANSPORTE_OFRECIDO')

			return redirect('feed')
	else:

		transport_post_form = TransportForm()
	
	context = {
		'transport_post_form' : transport_post_form
	}

	return render(request, 'publish-transport-post.html', context)





###################################################################
#	Vista de la publicacion de un contrato  					  #
###################################################################
@login_required
def publish_contract(request):

	current_user = get_object_or_404(CustomUser, pk = request.user.pk)

	if request.method == 'POST':

		contract_form = ContractForm(request.POST, request.FILES)

		if contract_form.is_valid():

			contract_form = contract_form.save(commit = False)
			contract_form.save()

			messages.success(request, message = 'MENSAJE_DOCUMENTO_SUBIDO')

			return redirect('feed')
	else:

		contract_form = ContractForm()
	
	context = {
		'contract_form' : contract_form
	}

	return render(request, 'publish-contract.html', context)



def contract(request):

	contracts = Contract.objects.filter().all()

	context = {
		'contracts' : contracts
	}

	return render(request, 'contract.html', context)



###################################################################
#	Vista de la cuenta bancaria del usuario						  #
###################################################################
@login_required
def bank_account(request):

	current_user = get_object_or_404(CustomUser, pk = request.user.pk)

	user = CustomUser.objects.get(username=current_user)

	#banks = BankAccount.objects.get(user=user)
	bank_account = BankAccount.objects.filter(user=user).order_by('-timestamp')

	paginator = Paginator(bank_account, 1)
	page = request.GET.get('page')
	bank_account= paginator.get_page(page)


	if request.method == 'POST':
		time.sleep(5)

		bank_account_form = BankAccountForm(request.POST)

		if bank_account_form.is_valid():

			
			bank_account_number_length = len(str(bank_account_form.cleaned_data['bank_account_number']))
			
			if bank_account_number_length <= 8:
				bank_account = bank_account_form.save(commit = False)
				bank_account.user = current_user
				bank_account.save()
			
				return redirect('bank_account')
			

	else:

		bank_account_form = BankAccountForm()

		try:
			owner_full_name = f'''{user.first_name} {user.last_name}'''.upper()
			bank_account_form.initial = {
				'owner_full_name' : owner_full_name
			}
		
		except Exception:
			pass

	return render(
		request, 'bank-account.html',
		{
			'user' : user,
			'bank_account' : bank_account,
			'bank_account_form' : bank_account_form,
		}
	)



###################################################################
#	Vista de la eliminacion de cuenta bancaria					  #
#	Recibe los argumentos	id_bank_account						  #
###################################################################
@login_required
def delete_bank_account(request, id_bank_account = None):
	time.sleep(2.5)

	bank_account = BankAccount.objects.get(id_bank_account = id_bank_account)
	print(bank_account)
	bank_account.delete()

	time.sleep(2.5)

	return redirect('bank_account')

###################################################################
#	Vista de la modificacion de cuenta bancaria					  #
#	Recibe los argumentos	id_bank_account						  #
###################################################################
###################################################################
###################################################################
#	En prueba													  #
###################################################################
@login_required
def modify_bank_account(request, id_bank_account = None):
	time.sleep(2.5)


	if request.method == 'POST':
		bank_account_form = BankAccountForm(request.POST)

		if bank_account_form.is_valid():
			bank_account_form.save()

	#bank = BankAccount.objects.get(id_bank_account=id_bank_account)
	#bank.save()

	time.sleep(2.5)

	return redirect('bank_account')

###################################################################
#	Vista de la publicacion de una solicitud de producto		  #
###################################################################
@login_required
def product_request(request):

	current_user = get_object_or_404(CustomUser, pk=request.user.pk)

	if request.method == 'POST':

		product_request_form = ProductRequestForm(request.POST)

		if product_request_form.is_valid():

			product_request_post = product_request_form.save(commit = False)
			product_request_post.user = current_user
			product_request_post.save()

			__message = str(
				f'''Hola {current_user.first_name}, {current_user.last_name}'''
				'''\n\nGracias por tu pedido. Está en espera hasta que confirmemos que algun usuario de tipo Productor te responda.'''
				'''\nMientras tanto, aquí tienes un recordatorio de lo que has pedido:'''
				f'''\n\tProducto: {product_request_form.cleaned_data['title']}'''
				f'''\n\tCantidad:{product_request_form.cleaned_data['quantity']}'''
				f'''\n\tFecha de solicitud:{product_request_form.cleaned_data['requested_date']}'''
				'''\n\n¡Gracias por usar Feria Virtual Maipo Grande!'''
			)

			try:
				send_mail(
					subject = 'FERIA VIRTUAL MAIPO GRANDE - Solicitud aceptada',
					message = __message,
					from_email = settings.EMAIL_HOST_USER,
					recipient_list = [current_user.email, ]
				)
			except Exception as exc:
				pass

			return redirect('client_request')
	else:

		product_request_form = ProductRequestForm()
	
	context = {'product_request_form' : product_request_form}

	return render(request, 'product-request.html', context)



###################################################################
#	Vista de las publicaciones de solicitud de producto			  #
###################################################################
@login_required
def client_request(request):

	current_user = request.user

	if current_user.type == 'PRODUCTOR':

		product_request = ProductRequest.objects.all()
		product_post = current_user.product.all()


		paginator = Paginator(product_request, 1)
		page = request.GET.get('page')
		product_request= paginator.get_page(page)

		context = {
			'product_request' : product_request,
			'product_post' : product_post
		}

		return render(request, 'client-request.html', context)

	
	elif current_user.type == 'CLIENTE EXTERNO' or current_user.type == 'CLIENTE INTERNO':

		product_request = ProductRequest.objects.filter(user_id = request.user.id).all()

		paginator = Paginator(product_request, 1)
		page = request.GET.get('page')
		product_request= paginator.get_page(page)

		context = {
			'product_request' : product_request
		}


		return render(request, 'client-request.html', context)
	
	elif current_user.type == 'TRANSPORTISTA':
		product_request = ProductRequest.objects.all()

		product_post = Product.objects.all()
		transport_post = Transport.objects.all()
		transaction = Transaction.objects.all()

		context = {
			'product_request' : product_request,
			'transport_post' : transport_post
		}

		return render(request, 'client-request.html', context)

	else:
		pass




###################################################################
#	Vista del estado de solicitud por parte del cliente			  #
###################################################################
##########################   CORREGIR	###########################
##########################   CORREGIR	###########################
##########################   CORREGIR	###########################
@login_required
def client_request_status(request):

	product_request_status = ProductRequestStatus.objects.all()
	print(product_request_status)

	context = {
		'product_request_status' : product_request_status
	}

	return render(request, 'client-request-status.html', context)


@login_required
def client_requests_status(request, id_product_request = None):

	#product_request_status = ProductRequestStatus.objects.filter(id_client = id_client).all()
	product_request_status = ProductRequestStatus.objects.filter(id_product_request_id = id_product_request).all()

	context = {
		'product_request_status' : product_request_status
	}

	return render(request, 'client-request-status.html', context)



###################################################################
#	Vista de recarga de saldo de la cuenta bancaria 			  #
###################################################################

def recharge(request):

	bank_account = BankAccount.objects.filter(user_id=request.user.id).all()


	messages.info(request, message = 'MENSAJE_ACLARACION_SERVICIO_RECARGA')
	context = {
		'bank_account' : bank_account
	}

	return render(request, 'recharge.html', context)

def recharge_amount(request, id_bank = None, recharge_amount = None):

	try:
		bank_account = BankAccount.objects.filter(id_bank_account = id_bank).get()
		bank_account.bank_amount += recharge_amount
	
	except BankAccount.DoesNotExist:
		bank_account = BankAccount.objects.first()
		bank_account.bank_amount += recharge_amount
	
	bank_account.save()


	recharge_transaction = RechargeTransaction(
		id_bank_account = id_bank,
		user = request.user,
		charge = recharge_amount + 2350
	)
	recharge_transaction.save()

	return redirect('bank_account')


###################################################################
#	Proceso de venta del producto ofrecido/recibido			  	  #
#	Recibe los argumentos	id_product							  #
###################################################################
@login_required
def decline_offered_product(request, id_product = None):

	status = 'RECHAZADO'

	offered_product = ProductRequestStatus.objects.filter(id_offered_product = id_product).first()
	offered_product.status = status
	offered_product.save()

	return redirect('client_request')



@login_required
def accept_offered_product(request, id_product = None):
	
	status = 'APROBADO'
	
	product_request_status = ProductRequestStatus.objects.get(id_offered_product = id_product)
	product_request_status.status = status
	product_request_status.save()
	
	current_user = get_object_or_404(CustomUser, pk = request.user.pk)


	if current_user.type == 'CLIENTE EXTERNO' or current_user.type == 'CLIENTE INTERNO':

		if request.method == 'POST':

			user = CustomUser.objects.get(username = current_user)
			product_post = Product.objects.get(id = id_product)
			bank_account = BankAccount.objects.filter(user = user)

			context = {
				'request' : request,
				'product_post' : product_post,
				'bank_account' : bank_account,
				'user' : user
			}

			print(context)
			
			return render(request, 'product-sale.html', context)

		else:

			user = CustomUser.objects.get(username = current_user)
			product_post = Product.objects.get(id = id_product)
			bank_account = BankAccount.objects.filter(user = user)

			context = {
				'request' : request,
				'product_post' : product_post,
				'bank_account' : bank_account,
				'user' : user
			}

			return render(request, 'product-sale.html', context)
	else:
		pass



@login_required
def delete_offered_product(request, id_offered_product = None):

	product_offer = ProductRequestStatus.objects.filter(id_offered_product = id_offered_product)
	product_offer.delete()

	return redirect('client_request')



###################################################################
#	Vista de la publicacion de una oferta de transporte			  #
###################################################################

def offer_transport(request, id_transaction = None, id_product = None):

	transaction = Transaction.objects.filter(id_transaction=id_transaction)
	product_post = Product.objects.filter(id = id_product)
	transport_post = Transport.objects.all()


	context = {
		'request' : request,
		'transactions' : transaction,
		'transports' : transport_post,
		'products' : product_post
	}
	return render(request, 'request-transport.html', context)

def transport_request(request, id_transaction = None, id_product = None, id_transport = None):


	transactions = Transaction.objects.get(id_transaction = id_transaction)
	product_post = Product.objects.get(id = id_product)
	transport_post = Transport.objects.get(id = id_transport)

	transactions.id_transport = transport_post.id
	transactions.transportist = f'{transport_post.user.first_name} {transport_post.user.last_name}'.upper()
	transactions.transport_status = 'SI'
	transactions.status = 'APROBADO'
	transactions.transport_type = transport_post.type
	transactions.transport_patent = transport_post.patent
	transactions.transport_capacity = transport_post.capacity
	transactions.transport_size = transport_post.size
	transactions.transport_refrigeration = transport_post.refrigeration
	transactions.save()

	transport_request_status = TransportRequestStatus(
		id_transaction = transactions.id_transaction,
		id_product = transactions.id_product,
		id_transport = transactions.id_transport,
		producer = transactions.producer,
		client = transactions.client,
		transportist = transactions.transportist,
		status = 'PEDIDO AUN NO PROCESADO',
		tracking_number = random.randint(10000000, 99999999)
	)
	transport_request_status.save()
	print(transport_request_status)

	return redirect('purchased_products')

######################################################################################################################################

###################################################################
#	Vista de la publicacion de una oferta de producto			  #
###################################################################
###################################################################
###################################################################
###################################################################
###################################################################
###################################################################
###################################################################
###################################################################
@login_required
def offer_product(request, id_offered_product = None, id_product_request = None):
	current_user = get_object_or_404(CustomUser, pk = request.user.pk)

	#to_user = CustomUser.objects.get(username=username)
	#to_user_id = to_user.id

	status = 'PENDIENTE'

	name_offered_product = request.user.product.get(id = id_offered_product)

	product_request_status = ProductRequestStatus(
		id_offered_product = id_offered_product,
		id_product_request_id = id_product_request,
		id_client = id_product_request,
		id_producer = current_user.id,
		id_offered_transport = 0,
		offered_product = str(name_offered_product),
		offered_transport = 'EN ESPERA DE ALGUN TRANSPORTE DISPONIBLE.',
		status = str(status)
	)
	product_request_status.save()
	
	__message = str(
		f'''Hola {current_user.first_name.upper()} {current_user.last_name.upper()}'''
		'''\n\nGracias por tu oferta. Está en espera hasta que confirmemos que exista alguna respuesta por parte del Cliente.'''
		'''\n\nMientras tanto, aquí tienes un recordatorio de lo que has ofrecido:'''
		f'''\n\tID del Producto: {id_offered_product}'''
		f'''\n\tCantidad:{name_offered_product}'''
		f'''\n\tEstado:{status}'''
		'''\n\n¡Gracias por usar Feria Virtual Maipo Grande!'''
	)

	try:
		send_mail(
			subject = f'FERIA VIRTUAL MAIPO GRANDE - Producto {id_offered_product} ofrecido {name_offered_product}',
			message = __message,
			from_email = settings.EMAIL_HOST_USER,
			recipient_list = [current_user.email, ]
		)
	except Exception as exc:
		pass


	return redirect('client_request')


###################################################################
#	Vista de las publicaciones de los transportes creados por	  #
# 	el usuario de tipo transportista							  #
###################################################################
@login_required
def transport(request):

	current_user = get_object_or_404(CustomUser, pk = request.user.pk)

	if current_user.type == 'TRANSPORTISTA':


		user = CustomUser.objects.get(username = current_user)


		#banks = BankAccount.objects.get(user=user)
		transports = Transport.objects.filter(user = user)


		return render(
			request, 'transport.html',
			{
				'user' : user,
				'transports' : transports,
			}
		)
	
	else:
		pass




###################################################################
#	Vista de la publicacion del producto creado por			  	  #
# 	el usuario de tipo transportista							  #
###################################################################
def view_product_post(request, id_product = None):

	#transactions = Transaction.objects.get(id_transaction=id_transaction)
	#posts = Product.objects.filter(id=transactions.product).get()
	product_post = Product.objects.filter(id=id_product)
	print(product_post)

	context = {'product_post' : product_post}

	return render(request, 'product.html', context)



def view_transport_post(request, id_transport = None):

	#transactions = Transaction.objects.get(id_transaction=id_transaction)
	#posts = Product.objects.filter(id=transactions.product).get()
	transport_post = Product.objects.filter(id=id_transport)

	context = {'product_post' : transport_post}

	return render(request, 'transport.html', context)


###################################################################
#	Vista del registro de usuario							  	  #
###################################################################
def signup(request):

	if request.method == 'POST':

		sign_up_form = SignUpForm(request.POST)

		if sign_up_form.is_valid():

			sign_up_form.cleaned_data['first_name'] = f'''{sign_up_form.cleaned_data['first_name']}'''.upper()
			sign_up_form.cleaned_data['last_name'] = f'''{sign_up_form.cleaned_data['last_name']}'''.upper()

			sign_up_form.save()

			__message = str(
				f'''Hola {str(sign_up_form.cleaned_data['first_name']).upper()} {str(sign_up_form.cleaned_data['last_name']).upper()}'''
				'''\n\nTe damos la bienvenida a Feria Virtual Maipo Grande. Tu nueva cuenta tiene acceso a los servicios asociados segun el tipo de usuario que escogiste.'''
				'''\n\n¡Gracias por usar Feria Virtual Maipo Grande!'''
			)


			try:
				send_mail(
					subject = 'FERIA VIRTUAL MAIPO GRANDE - Cuenta creada',
					message = __message,
					from_email = settings.EMAIL_HOST_USER,
					recipient_list = [sign_up_form.cleaned_data['email'], ]
				)
			except Exception as exc:
				pass
			
			return redirect('home')
	else:

		sign_up_form = SignUpForm()

	context = { 'sign_up_form' : sign_up_form }

	return render(request, 'signup.html', context)



###################################################################
#	Validacion del inicio de sesion de usuario				  	  #
###################################################################


def user_login(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            username=username,
            password=password
        )
		
        if user is not None:
            login(request, user)
            
            return render(request, 'profile.html')

        else:

            return render(request, 'login.html', {'error_message': 'Incorrect username and / or password.'})

    else:

        return render(request, 'login.html')



###################################################################
#	[ ! ]	Seguir a un usuario				  	  				  #
###################################################################
def follow(request, username):
	time.sleep(5)

	current_user = request.user
	to_user = CustomUser.objects.get(username=username)
	to_user_id = to_user

	rel = Relationship(from_user=current_user, to_user=to_user_id)
	rel.save()


	return redirect('feed')



###################################################################
#	[ ! ]	Dejar de seguir a un usuario	  	  				  #
###################################################################
def unfollow(request, username):
	current_user = request.user
	to_user = CustomUser.objects.get(username=username)
	to_user_id = to_user.id
	rel = Relationship.objects.filter(from_user=current_user.id, to_user=to_user_id)
	rel.delete()
	return redirect('feed')



###################################################################
#	Busqueda de producto					  	  				  #
###################################################################
def search_product(request):
	current_user = get_object_or_404(CustomUser, pk = request.user.pk)

	results = []

	if request.method == "GET":

		query = request.GET.get('search')
		
		if query == '':

			return redirect('feed')
		
		results = Product.objects.filter(
			Q(title__contains=query) |
			Q(owner_full_name__contains=query) |
			Q(user__username__contains=query) |
			Q(price__contains=query) |
			Q(quantity__contains=query)
		)
	context = {'query': query, 'results': results}
	return render(request, 'search-product.html', context)



###################################################################
#	Busqueda de producto comprado			  	  				  #
###################################################################
def search_purchased_product(request):
	current_user = get_object_or_404(CustomUser, pk = request.user.pk)

	results = []

	if request.method == "GET":

		query = request.GET.get('search')

		if query == '':

			return redirect('purchased_products')
		
		results = Transaction.objects.filter(
			Q(product__contains=query) |
			#Q(quantity__contains=query) |
			Q(producer__contains=query) |
			Q(client__contains=query) |
			Q(price__contains=query) |
			Q(total__contains=query) |
			Q(transport_status__contains=query) |
			Q(transport_type__contains=query) |
			Q(transport_refrigeration__contains=query) |
			Q(status__contains=query) 

		)
	context = {'query': query, 'results': results}
	return render(request, 'search-purchased-product.html', context)



###################################################################
#	Busqueda de solicitud de producto		  	  				  #
###################################################################
def search_product_request(request):

	results = []

	if request.method == "GET":

		query = request.GET.get('search')

		if query == '':
			return redirect('client_request_status')
		
		results = ProductRequestStatus.objects.filter(
			Q(offered_product__contains = query) |
			Q(status__contains = query)
		)
	context = {'query': query, 'results': results}

	return render(request, 'search-product-request.html', context)



###################################################################
#	Producto vendido						  	  				  #
###################################################################
def product_sold(request, id_product = None):
	current_user = get_object_or_404(CustomUser, pk = request.user.pk)

	product = Product.objects.filter(id=id_product).first()
	purchased_product = Transaction.objects.filter(product=product.title)

	context = {'purchased_product' : purchased_product}
	return render(request, 'purchased-product.html', context)



###################################################################
#	Prodcutos comprados						  	  				  #
###################################################################
def purchased_products(request):
	current_user = get_object_or_404(CustomUser, pk = request.user.pk)

	user_full_name = f'{current_user.first_name} {current_user.last_name}'.upper()

	if current_user.type == 'CLIENTE EXTERNO' or current_user.type == 'CLIENTE INTERNO':
		client_full_name = user_full_name
		print(client_full_name)
		print(client_full_name)
		print(client_full_name)
		print(client_full_name)
		print(client_full_name)
		print(client_full_name)

		purchased_product = Transaction.objects.filter(client = client_full_name).all()
	
	elif current_user.type == 'PRODUCTOR':
		producer_full_name = user_full_name
		purchased_product = Transaction.objects.filter(producer = producer_full_name)
	
	elif current_user.type == 'CONSULTOR' or current_user.type == 'TRANSPORTISTA':
		purchased_product = Transaction.objects.all()
	
	elif current_user.type == 'TRANSPORTISTA':
		purchased_product = Transaction.objects.all()


	context = {'purchased_product' : purchased_product}

	return render(request, 'purchased-product.html', context)



def order_tracking(request, id_transaction = None, id_product = None):

	transactions = Transaction.objects.filter(id_transaction = id_transaction).all()
	transaction_status = TransportRequestStatus.objects.filter(id_transaction = id_transaction).all()


	context = {
		'transactions' : transactions,
		'transaction_status' : transaction_status
	}

	return render(request, 'order-tracking.html', context)


def switch_to_order_tracking_status_1(request, id_transaction = None, id_product = None):
	transactions = Transaction.objects.filter(id_transaction = id_transaction).all()
	transaction_status = TransportRequestStatus.objects.filter(id_transaction = id_transaction).get()
	transaction_status.status = TRACKING_STATUS[1][0]
	transaction_status.save()

	transaction_status = TransportRequestStatus.objects.filter(id_transaction = id_transaction).all()



	try:
		###################################################################
		#	Mensaje hacia el usuario productor						      #
		###################################################################

		transaction = Transaction.objects.get(id_transaction = id_transaction)
		producer_user_full_name = transaction.producer
		client_user_full_name = transaction.client


		__message = str(
			f'''Hola {producer_user_full_name}'''
			f'''\n\nLa transaccion #{id_transaction} está en proceso.'''
			'''\nSe te informará los cambios que realice el transportista.'''
			'''\n\n¡Gracias por usar Feria Virtual Maipo Grande!'''
		)
			
		###################################################################
		#	Manejo de excepcion en caso de que hayan problemas con la     #
		#	seguridad de la cuenta google de maipo.grande.object          #
		#															      #
		#	en caso de haber un problema, usar este link:                 #
		#	https://myaccount.google.com/security?hl=es_419               #
		#																  #
		#	Dirigirse a "Acceso a Google"								  #
		#	Verificacion en 2 pasos      SI								  #
		#	Contraseñas de aplicaciones	 (como requisito deberia haber 1) #
		###################################################################


		__producer_user_full_name = producer_user_full_name.split(' ')
		__producer_user_first_name = __producer_user_full_name[0] + ' ' + __producer_user_full_name[1]
		__producer_user_last_name = __producer_user_full_name[2] + ' ' + __producer_user_full_name[3]

		
		try:
			user = CustomUser.objects.get(first_name = __producer_user_first_name, last_name = __producer_user_last_name)

			send_mail(
				subject = f'''FERIA VIRTUAL MAIPO GRANDE - Producto {transaction.product} - Envio en proceso''',
				message = __message,
				from_email = settings.EMAIL_HOST_USER,
				recipient_list = [user.email, ]
			)
			
		except Exception as exc:
			pass



		__message = str(
			f'''Hola {client_user_full_name}'''
			f'''\n\nLa orden de la transaccion #{id_transaction} está en proceso.'''
			'''\nSe te informará los cambios que realice el transportista.'''
			'''\n\n¡Gracias por usar Feria Virtual Maipo Grande!'''
		)
			
		###################################################################
		#	Manejo de excepcion en caso de que hayan problemas con la     #
		#	seguridad de la cuenta google de maipo.grande.object          #
		#															      #
		#	en caso de haber un problema, usar este link:                 #
		#	https://myaccount.google.com/security?hl=es_419               #
		#																  #
		#	Dirigirse a "Acceso a Google"								  #
		#	Verificacion en 2 pasos      SI								  #
		#	Contraseñas de aplicaciones	 (como requisito deberia haber 1) #
		###################################################################


		__client_user_full_name = client_user_full_name.split(' ')
		__client_user_first_name = __client_user_full_name[0] + ' ' + __client_user_full_name[1]
		__client_user_last_name = __client_user_full_name[2] + ' ' + __client_user_full_name[3]


		
		
		try:
			user = CustomUser.objects.get(first_name = __client_user_first_name, last_name = __client_user_last_name)

			send_mail(
				subject = f'''FERIA VIRTUAL MAIPO GRANDE - Producto {transaction.product} - Envio en proceso''',
				message = __message,
				from_email = settings.EMAIL_HOST_USER,
				recipient_list = [user.email, ]
			)
			
		except Exception as exc:
			pass



	except Exception as exc:
		pass


	context = {
		'transactions' : transactions,
		'transaction_status' : transaction_status
	}
	return render(request, 'order-tracking.html', context)

def switch_to_order_tracking_status_2(request, id_transaction = None, id_product = None):
	transactions = Transaction.objects.filter(id_transaction = id_transaction).all()
	transaction_status = TransportRequestStatus.objects.filter(id_transaction = id_transaction).get()
	transaction_status.status = TRACKING_STATUS[2][0]
	transaction_status.save()


	transaction_status = TransportRequestStatus.objects.filter(id_transaction = id_transaction).all()


	try:
		###################################################################
		#	Mensaje hacia el usuario productor						      #
		###################################################################

		transaction = Transaction.objects.get(id_transaction = id_transaction)
		producer_user_full_name = transaction.producer
		client_user_full_name = transaction.client


		__message = str(
			f'''Hola {producer_user_full_name}'''
			f'''\n\nLa transaccion #{id_transaction} está en tránsito.'''
			'''\nSe te informará los cambios que realice el transportista.'''
			'''\n\n¡Gracias por usar Feria Virtual Maipo Grande!'''
		)
			
		###################################################################
		#	Manejo de excepcion en caso de que hayan problemas con la     #
		#	seguridad de la cuenta google de maipo.grande.object          #
		#															      #
		#	en caso de haber un problema, usar este link:                 #
		#	https://myaccount.google.com/security?hl=es_419               #
		#																  #
		#	Dirigirse a "Acceso a Google"								  #
		#	Verificacion en 2 pasos      SI								  #
		#	Contraseñas de aplicaciones	 (como requisito deberia haber 1) #
		###################################################################


		__producer_user_full_name = producer_user_full_name.split(' ')
		__producer_user_first_name = __producer_user_full_name[0] + ' ' + __producer_user_full_name[1]
		__producer_user_last_name = __producer_user_full_name[2] + ' ' + __producer_user_full_name[3]

		
		try:
			user = CustomUser.objects.get(first_name = __producer_user_first_name, last_name = __producer_user_last_name)

			send_mail(
				subject = f'''FERIA VIRTUAL MAIPO GRANDE - Producto {transaction.product} - Envio en tránsito''',
				message = __message,
				from_email = settings.EMAIL_HOST_USER,
				recipient_list = [user.email, ]
			)
			
		except Exception as exc:
			pass



		__message = str(
			f'''Hola {client_user_full_name}'''
			f'''\n\nLa orden de la transaccion #{id_transaction} está en tránsito.'''
			'''\nSe te informará los cambios que realice el transportista.'''
			'''\n\n¡Gracias por usar Feria Virtual Maipo Grande!'''
		)
			
		###################################################################
		#	Manejo de excepcion en caso de que hayan problemas con la     #
		#	seguridad de la cuenta google de maipo.grande.object          #
		#															      #
		#	en caso de haber un problema, usar este link:                 #
		#	https://myaccount.google.com/security?hl=es_419               #
		#																  #
		#	Dirigirse a "Acceso a Google"								  #
		#	Verificacion en 2 pasos      SI								  #
		#	Contraseñas de aplicaciones	 (como requisito deberia haber 1) #
		###################################################################


		__client_user_full_name = client_user_full_name.split(' ')
		__client_user_first_name = __client_user_full_name[0] + ' ' + __client_user_full_name[1]
		__client_user_last_name = __client_user_full_name[2] + ' ' + __client_user_full_name[3]


		
		
		try:
			user = CustomUser.objects.get(first_name = __client_user_first_name, last_name = __client_user_last_name)

			send_mail(
				subject = f'''FERIA VIRTUAL MAIPO GRANDE - Producto {transaction.product} - Envio en tránsito''',
				message = __message,
				from_email = settings.EMAIL_HOST_USER,
				recipient_list = [user.email, ]
			)
			
		except Exception as exc:
			pass



	except Exception as exc:
		pass



	context = {
		'transactions' : transactions,
		'transaction_status' : transaction_status
	}
	return render(request, 'order-tracking.html', context)

def switch_to_order_tracking_status_3(request, id_transaction = None, id_product = None):
	transactions = Transaction.objects.filter(id_transaction = id_transaction).all()
	transaction_status = TransportRequestStatus.objects.filter(id_transaction = id_transaction).get()
	transaction_status.status = TRACKING_STATUS[3][0]
	transaction_status.save()

	transaction_status = TransportRequestStatus.objects.filter(id_transaction = id_transaction).all()


	try:
		###################################################################
		#	Mensaje hacia el usuario productor						      #
		###################################################################

		transaction = Transaction.objects.get(id_transaction = id_transaction)
		producer_user_full_name = transaction.producer
		client_user_full_name = transaction.client


		__message = str(
			f'''Hola {producer_user_full_name}'''
			f'''\n\nLa transaccion #{id_transaction} ha sido finalizada, el comprador ya recibio su orden,'''
			'''\n\n¡Gracias por usar Feria Virtual Maipo Grande!'''
		)
			
		###################################################################
		#	Manejo de excepcion en caso de que hayan problemas con la     #
		#	seguridad de la cuenta google de maipo.grande.object          #
		#															      #
		#	en caso de haber un problema, usar este link:                 #
		#	https://myaccount.google.com/security?hl=es_419               #
		#																  #
		#	Dirigirse a "Acceso a Google"								  #
		#	Verificacion en 2 pasos      SI								  #
		#	Contraseñas de aplicaciones	 (como requisito deberia haber 1) #
		###################################################################


		__producer_user_full_name = producer_user_full_name.split(' ')
		__producer_user_first_name = __producer_user_full_name[0] + ' ' + __producer_user_full_name[1]
		__producer_user_last_name = __producer_user_full_name[2] + ' ' + __producer_user_full_name[3]

		
		try:
			user = CustomUser.objects.get(first_name = __producer_user_first_name, last_name = __producer_user_last_name)

			send_mail(
				subject = f'''FERIA VIRTUAL MAIPO GRANDE - Producto {transaction.product} - Envio entregado''',
				message = __message,
				from_email = settings.EMAIL_HOST_USER,
				recipient_list = [user.email, ]
			)
			
		except Exception as exc:
			pass



		__message = str(
			f'''Hola {client_user_full_name}'''
			f'''\n\nLa transaccion #{id_transaction} ha sido finalizada, el pedido ya ha sido entregado en la direccion indicada,'''
			'''\n\n¡Gracias por usar Feria Virtual Maipo Grande!'''
		)
			
		###################################################################
		#	Manejo de excepcion en caso de que hayan problemas con la     #
		#	seguridad de la cuenta google de maipo.grande.object          #
		#															      #
		#	en caso de haber un problema, usar este link:                 #
		#	https://myaccount.google.com/security?hl=es_419               #
		#																  #
		#	Dirigirse a "Acceso a Google"								  #
		#	Verificacion en 2 pasos      SI								  #
		#	Contraseñas de aplicaciones	 (como requisito deberia haber 1) #
		###################################################################


		__client_user_full_name = client_user_full_name.split(' ')
		__client_user_first_name = __client_user_full_name[0] + ' ' + __client_user_full_name[1]
		__client_user_last_name = __client_user_full_name[2] + ' ' + __client_user_full_name[3]


		
		
		try:
			user = CustomUser.objects.get(first_name = __client_user_first_name, last_name = __client_user_last_name)

			send_mail(
				subject = f'''FERIA VIRTUAL MAIPO GRANDE - Producto {transaction.product} - Envio entregado''',
				message = __message,
				from_email = settings.EMAIL_HOST_USER,
				recipient_list = [user.email, ]
			)
			
		except Exception as exc:
			pass



	except Exception as exc:
		pass



	context = {
		'transactions' : transactions,
		'transaction_status' : transaction_status
	}
	return render(request, 'order-tracking.html', context)

def switch_to_order_tracking_status_0(request, id_transaction = None, id_product = None):
	transactions = Transaction.objects.filter(id_transaction = id_transaction).all()
	transaction_status = TransportRequestStatus.objects.filter(id_transaction = id_transaction).get()
	transaction_status.status = TRACKING_STATUS[0][0]
	transaction_status.save()
	
	transaction_status = TransportRequestStatus.objects.filter(id_transaction = id_transaction).all()


	context = {
		'transactions' : transactions,
		'transaction_status' : transaction_status
	}
	return render(request, 'order-tracking.html', context)



def international_contract_sales_process(request):
	try:
		international_contract = InternationalContract(
			international_contract = ANSWER[0][0]
		)
		international_contract.save()
	
	except:
		pass

	contract = InternationalContract.objects.get(international_contract = ANSWER[0][0])
	contract.contract_validity = ANSWER[1][0]
	contract.save()

	messages.success(request, message = 'MENSAJE_PROCESO_VENTA_INTERNACIONAL_REALIZADA')


	return redirect('feed')





@login_required
def international_contract_process(request):

	current_user = get_object_or_404(CustomUser, pk = request.user.pk)

	user = CustomUser.objects.get(username=current_user)

	international_contract = InternationalContract.objects.all()

	paginator = Paginator(international_contract, 1)
	page = request.GET.get('page')
	international_contract= paginator.get_page(page)


	if request.method == 'POST':
		time.sleep(5)

		international_contract_form = InternationalContractForm(request.POST)

		if international_contract_form.is_valid():
			international_contract_form.save()
			return redirect('international_contract_process')
			

	else:

		international_contract_form = InternationalContractForm()

	return render(
		request, 'international-contract-process.html',
		{
			'user' : user,
			'international_contract' : international_contract,
			'international_contract_form' : international_contract_form,
		}
	)


@login_required
def delete_international_contract(request, id_contract = None):
	time.sleep(2.5)

	international_contract = InternationalContract.objects.get(id = id_contract)
	international_contract.delete()

	time.sleep(2.5)

	return redirect('international_contract_process')

@login_required
def renew_international_contract(request, id_contract = None):
	time.sleep(2.5)

	international_contract = InternationalContract.objects.get(id = id_contract)
	international_contract.contract_validity = ANSWER[1][0]
	international_contract.save()

	time.sleep(2.5)

	return redirect('international_contract_process')

@login_required
def revoke_international_contract(request, id_contract = None):
	time.sleep(2.5)

	international_contract = InternationalContract.objects.get(id = id_contract)
	international_contract.contract_validity = ANSWER[0][0]
	international_contract.save()

	time.sleep(2.5)

	return redirect('international_contract_process')









@login_required
def total_transactions_made(request):


	current_user = get_object_or_404(CustomUser, pk = request.user.pk)

	user_full_name = f'{current_user.first_name} {current_user.last_name}'.upper()

	producer_full_name = user_full_name
	purchased_product = Transaction.objects.filter(producer = producer_full_name, status = 'APROBADO')


	total = 0

	for transaction in purchased_product.all():
		total += transaction.total
	
	__service = int(total * (15/100))
	total -= __service



	context = {'total' : total}

	return render(request, 'total-transactions.html', context)



def generate_contract(request):
	current_user = get_object_or_404(CustomUser, pk = request.user.pk)

	transactions = Transaction.objects.filter(status = 'APROBADO').all().order_by('-timestamp')

	paginator = Paginator(transactions, 1)
	page = request.GET.get('page')
	transactions = paginator.get_page(page)

	context = {'transactions' : transactions}

	return render(request, 'generate-contract.html', context)