from django.contrib.auth import authenticate, login

from django.shortcuts import render, redirect, get_object_or_404

from .models import (
    CustomUser,
	ProductRequest,
	Profile,
	Relationship,
	Product,
	BankAccount,
	ProductRequestStatus,
	Transport,
	Transaction
)
from .forms import (
    BankAccountForm,
	ContactForm,
	ProductRequestForm,
	SignUpForm,
	ProductForm, 
	TransportForm
)

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings
from django.db import connection



#	Principal
def home(request):

	if request.method == 'POST':
	
		form = ContactForm(request.POST)

		if form.is_valid():

			form.save()

			return redirect('home')
	else:

		form = ContactForm()

	context = { 'form' : form }
 
	return render(request, 'home.html', context)



#	Iniciar sesion
def login(request):
    return render(request, 'login.html')



#	Perfil de usuario
@login_required
def profile(request, username = None):

	current_user = request.user

	# if username and username != current_user.username
	if username != current_user:

		user = CustomUser.objects.get(username=username)
		posts = user.posts.all()

	else:

		posts = current_user.posts.all()
		user = current_user
  
	return render(request, 'profile.html', {'user':user, 'posts':posts})



#	Publicar producto
@login_required
def post_product(request):

	current_user = get_object_or_404(CustomUser, pk=request.user.pk)
	user = CustomUser.objects.get(username=current_user)

	if request.method == 'POST':

		form = ProductForm(request.POST, request.FILES)#eliminar request.FILES si hay problema

		if form.is_valid():

			post = form.save(commit=False)
			post.user = current_user
			post.save()

			__message = str(
				f'Hola {current_user.first_name.upper()} {current_user.last_name.upper()}\n'
				'Gracias por tu oferta. Se ha publicado tu producto y ahora está en espera hasta que confirmemos que exista alguna respuesta.\n'
				'Mientras tanto, aquí tienes un recordatorio de lo que has ofrecido:\n'
				f"\tProducto: {form.cleaned_data['title']}\n"
				f"\tDescripcion:{form.cleaned_data['description']}\n"
				f"\tCantidad:{form.cleaned_data['quantity']}\n"
				'¡Gracias por usar Feria Virtual Maipo Grande!\n'
			)

			send_mail(
				subject = f'''FERIA VIRTUAL MAIPO GRANDE - Producto {form.cleaned_data['title']} ofrecido''',
				message = __message,
				from_email = settings.EMAIL_HOST_USER,
				recipient_list = [current_user.email, ]
			)

			return redirect('feed')

	else:

		form = ProductForm()

		try:
			#obj = banks.first()
			#owner_full_name = str(getattr(obj, 'owner_full_name')).upper()

			owner_full_name = f'{user.first_name} {user.last_name}'.upper()
			form.initial = {
				'owner_full_name' : owner_full_name
			}
		
		except Exception:
			pass
		
	return render(request, 'post-product.html', {'form' : form })


@login_required
def product_sale(request, id_product = None):
	current_user = get_object_or_404(CustomUser, pk = request.user.pk)

	if current_user.type == 'CLIENTE EXTERNO' or current_user.type == 'CLIENTE INTERNO':

		if request.method == 'POST':
			user = CustomUser.objects.get(username=current_user)
			product = Product.objects.get(id=id_product)
			banks = BankAccount.objects.filter(user=user)
			
			return render(request, 'product-sale.html', {'request' : request,'product' : product, 'banks' : banks, 'user' : user})

		else:

			user = CustomUser.objects.get(username=current_user)
			product = Product.objects.get(id=id_product)
			banks = BankAccount.objects.filter(user=user)

			
			return render(request, 'product-sale.html', {'request' : request,'product' : product, 'banks' : banks, 'user' : user})
	else:
		pass


# Venta efectuada
@login_required
def product_sales_transaction(
	request, id_bank_account = None, amount = None,
	id_product = None, quantity = None, id_producer = None, id_client = None, price = None):

	current_user = get_object_or_404(CustomUser, pk = request.user.pk)
	user = CustomUser.objects.get(username=current_user)

	#banks = BankAccount.objects.get(user=user)
	bank = BankAccount.objects.get(id_bank_account=id_bank_account)

	if bank.bank_amount > amount:
		bank.bank_amount = bank.bank_amount - amount
	
	elif bank.bank_amount < amount:
		bank.bank_amount = amount - bank.bank_amount
	bank.save()

	product = Product.objects.get(id=id_product)
	product.quantity -= quantity

	if product.quantity < 0:
		product.quantity = 0

	product.save()

	transaction = Transaction(
		product = Product.objects.get(id=id_product).title,
		quantity = quantity,
		producer = str(f'{Profile.objects.get(id=id_producer).user.first_name} {Profile.objects.get(id=id_producer).user.last_name}').upper(),
		client = str(f'{Profile.objects.get(id=id_client).user.first_name} {Profile.objects.get(id=id_client).user.last_name}').upper(),
		price = price,
		total = amount,
		status = True
	)
	transaction.save()


	__message = str(
		f'''Hola {str(f'{Profile.objects.get(id=id_producer).user.first_name} {Profile.objects.get(id=id_producer).user.last_name}').upper()}\n'''
		f'''El usuario {str(f'{Profile.objects.get(id=id_client).user.username}')} con nombre {str(f'{Profile.objects.get(id=id_client).user.first_name} {Profile.objects.get(id=id_client).user.last_name}').upper()}\n'''
		f'''Ha comprado tu producto {Product.objects.get(id=id_product).title} y ahora está en espera hasta que confirmemos que exista algun transportista que pueda .\n'''
		'Mientras tanto, aquí tienes un resumen de la venta realizada:\n'

		f'''\n\tProducto {Product.objects.get(id=id_product).title}'''
		f'''\n\tCantidad {quantity}'''
		f'''\n\tTotal {amount}'''
		'\n\n¡Gracias por usar Feria Virtual Maipo Grande!\n'
	)

	send_mail(
		subject = f'''FERIA VIRTUAL MAIPO GRANDE - Producto {Product.objects.get(id=id_product).title} vendido''',
		message = __message,
		from_email = settings.EMAIL_HOST_USER,
		recipient_list = [Profile.objects.get(id=id_producer).user.email, ]
	)


	__message = str(
		f'''Hola {str(f'{Profile.objects.get(id=id_client).user.first_name} {Profile.objects.get(id=id_client).user.last_name}').upper()} \n'''
		f'''Se ha procesado exitosamente tu compra del producto {Product.objects.get(id=id_product).title} y ahora está en espera hasta que confirmemos que exista algun transportista que este operativo.\n'''
		'Mientras tanto, aquí tienes un resumen de la compra realizada:\n'

		f'''\n\tProducto {Product.objects.get(id=id_product).title}'''
		f'''\n\tCantidad {quantity}'''
		f'''\n\tTotal ${amount}'''
		'\n\n¡Gracias por usar Feria Virtual Maipo Grande!\n'
	)

	send_mail(
		subject = f'''FERIA VIRTUAL MAIPO GRANDE - Producto {Product.objects.get(id=id_product).title} comprado''',
		message = __message,
		from_email = settings.EMAIL_HOST_USER,
		recipient_list = [Profile.objects.get(id=id_client).user.email, ]
	)


	return redirect('feed')



#	Publicar transporte
@login_required
def post_transport(request):

	current_user = get_object_or_404(CustomUser, pk = request.user.pk)

	if request.method == 'POST':

		form = TransportForm(request.POST, request.FILES)

		if form.is_valid():

			post = form.save(commit=False)
			post.user = current_user
			post.save()

			return redirect('feed')
	else:

		form = TransportForm()

	return render(request, 'post-transport.html', {'form' : form })



#	Vista de la cuenta bancaria
@login_required
def bank_account(request):

	current_user = get_object_or_404(CustomUser, pk = request.user.pk)

	user = CustomUser.objects.get(username=current_user)

	#banks = BankAccount.objects.get(user=user)
	banks = BankAccount.objects.filter(user=user)

	if request.method == 'POST':


		form = BankAccountForm(request.POST)

		if form.is_valid():

			bank = form.save(commit=False)
			bank.user = current_user
			bank.save()

			return redirect('bank')

	else:

		form = BankAccountForm()

		try:
			#obj = banks.first()
			#owner_full_name = str(getattr(obj, 'owner_full_name')).upper()

			owner_full_name = f'{user.first_name} {user.last_name}'.upper()
			form.initial = {
				'owner_full_name' : owner_full_name
			}
		
		except Exception:
			pass




	return render(
		request, 'bank.html',
		{
			'user' : user,
			'banks' : banks,
			'form' : form,
		}
	)






#	Eliminar cuenta bancaria
@login_required
def delete_bank_account(request, id_bank_account = None):

	bank = BankAccount.objects.filter(pk=id_bank_account)
	bank.delete()
	return redirect('bank')



#	Solicitar producto
@login_required
def product_request(request):

	current_user = get_object_or_404(CustomUser, pk=request.user.pk)

	if request.method == 'POST':

		form = ProductRequestForm(request.POST)

		if form.is_valid():

			post = form.save(commit=False)
			post.user = current_user
			post.save()

			__message = str(
				f'Hola {current_user.first_name}, {current_user.last_name}\n'
				'Gracias por tu pedido. Está en espera hasta que confirmemos que algun usuario de tipo Productor te responda. Mientras tanto, aquí tienes un recordatorio de lo que has pedido:\n'
				f"\tProducto: {form.cleaned_data['title']}\n"
				f"\tCantidad:{form.cleaned_data['quantity']}\n"
				f"\tFecha de solicitud:{form.cleaned_data['requested_date']}\n\n"
				'¡Gracias por usar Feria Virtual Maipo Grande!\n'

			)
				

			send_mail(
				subject = 'FERIA VIRTUAL MAIPO GRANDE - Solicitud aceptada',
				message = __message,
                from_email = settings.EMAIL_HOST_USER,
				recipient_list = [current_user.email, ]
			)

			return redirect('request')
	else:

		form = ProductRequestForm()

	return render(request, 'product-request.html', {'form' : form })



#	Solicitudes de producto
@login_required
def client_request(request):

	current_user = request.user

	if current_user.type == 'PRODUCTOR':

		requests = ProductRequest.objects.all()
		products = current_user.posts.all()


		paginator = Paginator(requests, 1)
		page = request.GET.get('page')
		requests= paginator.get_page(page)

	
	elif current_user.type == 'CLIENTE EXTERNO' or current_user.type == 'CLIENTE INTERNO':
		#requests = current_user.posts.all()
		
		requests = ProductRequest.objects.filter(user = current_user.id)
		products = current_user
	
	else:

		pass

	return render(request, 'request.html', {'products' : products, 'requests' : requests})



#	Vista del estado de solicitud por parte del cliente
@login_required
def client_request_status(request):

	#requests = ProductRequestStatus.objects.filter(id = id_offered_product)
	requests = ProductRequestStatus.objects.all()
	print(requests)

	return render(request, 'request-status.html', {'requests' : requests})



#	Proceso de venta del producto ofrecido/recibido
@login_required
def decline_product_offer(request, id_offered_product = None):

	status = 'RECHAZADO'

	product_offer = ProductRequestStatus.objects.get(id_offered_product = id_offered_product)
	product_offer.status = status
	product_offer.save()

	return redirect('request')

@login_required
def accept_product_offer(request, id_offered_product = None):
	status = 'APROBADO'

	product_offer = ProductRequestStatus.objects.get(id_offered_product = id_offered_product)
	product_offer.status = status
	product_offer.save()

	return redirect('request')

@login_required
def delete_product_offer(request, id_offered_product = None):

	product_offer = ProductRequestStatus.objects.filter(id_offered_product = id_offered_product)
	product_offer.delete()

	return redirect('request')



#	Producto ofrecido
@login_required
def offer_product(request, id_offered_product = None):
	current_user = get_object_or_404(CustomUser, pk = request.user.pk)

	#to_user = CustomUser.objects.get(username=username)
	#to_user_id = to_user.id


	status = 'PENDIENTE'

	name_offered_product = request.user.posts.get(id = id_offered_product)

	product = ProductRequestStatus(
		id_offered_product = id_offered_product,
		offer = str(name_offered_product),
		status = str(status)
	)
	product.save()
	
	__message = str(
		f'Hola {current_user.first_name.upper()} {current_user.last_name.upper()}\n'
		'Gracias por tu oferta. Está en espera hasta que confirmemos que exista alguna respuesta por parte del Cliente. Mientras tanto, aquí tienes un recordatorio de lo que has ofrecido:\n'
		f"\tID del Producto: {id_offered_product}\n"
		f"\tCantidad:{name_offered_product}\n"
		f"\tEstado:{status}\n\n"
		'¡Gracias por usar Feria Virtual Maipo Grande!\n'
	)

	send_mail(
		subject = f'FERIA VIRTUAL MAIPO GRANDE - Producto {id_offered_product} ofrecido {name_offered_product}',
		message = __message,
        from_email = settings.EMAIL_HOST_USER,
		recipient_list = [current_user.email, ]
	)


	return redirect('request')



#	Transportes creados por el usuario de tipo TRANSPORTISTA
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


#	Publicaciones de producto
@login_required
def feed(request):

	posts = Product.objects.all()

	context = {'posts': posts}

	return render(request, 'feed.html', context)



#	Registro de usuario
def register(request):

	if request.method == 'POST':

		form = SignUpForm(request.POST)

		if form.is_valid():

			form.cleaned_data['first_name'] = str(form.cleaned_data['first_name']).upper()
			form.cleaned_data['last_name'] = str(form.cleaned_data['last_name']).upper()

			form.save()

			__message = str(
				f"Hola {str(form.cleaned_data['first_name']).upper(), str(form.cleaned_data['last_name']).upper()}\n"
				'Te damos la bienvenida a Feria Virtual Maipo Grande. Tu nueva cuenta tiene acceso a los servicios asociados segun el tipo de usuario que escogiste.\n\n'
				'¡Gracias por usar Feria Virtual Maipo Grande!\n'
			)

			send_mail(
				subject = 'FERIA VIRTUAL MAIPO GRANDE - Cuenta creada',
				message = __message,
                from_email = settings.EMAIL_HOST_USER,
				recipient_list = [form.cleaned_data['email'], ]
			)

			return redirect('home')
	else:

		form = SignUpForm()

	context = { 'form' : form }

	return render(request, 'register.html', context)



#	Iniciar sesion
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



#	Seguir usuario
def follow(request, username):
	current_user = request.user
	to_user = CustomUser.objects.get(username=username)
	to_user_id = to_user
	rel = Relationship(from_user=current_user, to_user=to_user_id)
	rel.save()
	return redirect('feed')

def unfollow(request, username):
	current_user = request.user
	to_user = CustomUser.objects.get(username=username)
	to_user_id = to_user.id
	rel = Relationship.objects.filter(from_user=current_user.id, to_user=to_user_id)
	rel.delete()
	return redirect('feed')



#	Buscar publicaciones
def search_product(request):
	current_user = get_object_or_404(CustomUser, pk = request.user.pk)

	results = []

	if request.method == "GET":

		query = request.GET.get('search')
		
		if query == '':

			return redirect('feed')
		
		results = Product.objects.filter(
			Q(title__contains=query) |
			Q(user__username__contains=query) |
			Q(price__contains=query)
		)
	
	return render(request, 'search-product.html', {'query': query, 'results': results})

def search_product_request(request):

	results = []

	if request.method == "GET":

		query = request.GET.get('search')

		if query == '':
			return redirect('client_request_status')
		
		results = ProductRequestStatus.objects.filter(
			Q(id_offered_product__contains = query) |
			Q(offer__contains = query) |
			Q(status__contains = query)
		)
	
	return render(request, 'search-product-request.html', {'query': query, 'results': results})


def purchased_products(request):
	current_user = get_object_or_404(CustomUser, pk = request.user.pk)

	if current_user.type == 'CLIENTE EXTERNO' or current_user.type == 'CLIENTE INTERNO':
		client_full_name = f'{str(current_user.first_name).upper()} {str(current_user.last_name).upper()}'
		print(client_full_name)
		#purchased_product = Transaction.objects.all().filter(client=client_full_name)
		purchased_product = Transaction.objects.filter(client=client_full_name)
		print(purchased_product)


	__connection = connection
	__cursor = __connection.cursor()
	#__cursor.execute("select * from maipogrande_transaction")
	__cursor.execute(
		'''
		DECLARE
			transaction maipogrande_transaction%TYPE;
		BEGIN
			SELECT * INTO transaction
			FROM maipogrande_transaction
			WHERE status = "APROBADO";
			dbms_output.put_line( transaction );
		END;
		'''
	)

	print(__cursor.fetchall())

	return render(request, 'purchased-product.html', {'purchased_product' : purchased_product})


# API REST
from rest_framework import viewsets

from .serializers import (
	CustomUserSerializer,
	ProductRequestSerializer,
	ProfileSerializer,
	ProductSerializer,
	BankAccountSerializer,
	ProductRequestStatusSerializer,
	TransportSerializer
)

class CustomUserViewSet(viewsets.ModelViewSet):
	queryset = CustomUser.objects.all()
	serializer_class = CustomUserSerializer

class ProductRequestViewSet(viewsets.ModelViewSet):
	queryset = ProductRequest.objects.all()
	serializer_class = ProductRequestSerializer

class ProfileViewSet(viewsets.ModelViewSet):
	queryset = Profile.objects.all()
	serializer_class = ProfileSerializer

class ProductViewSet(viewsets.ModelViewSet):
	queryset = Product.objects.all()
	serializer_class = ProductSerializer

class BankAccountViewSet(viewsets.ModelViewSet):
	queryset = BankAccount.objects.all()
	serializer_class = BankAccountSerializer

class ProductRequestStatusViewSet(viewsets.ModelViewSet):
	queryset = ProductRequestStatus.objects.all()
	serializer_class = ProductRequestStatusSerializer

class TransportViewSet(viewsets.ModelViewSet):
	queryset = Transport.objects.all()
	serializer_class = TransportSerializer