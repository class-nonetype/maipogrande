from django.contrib.auth import authenticate, login

from django.shortcuts import render, redirect, get_object_or_404

from .models import (
    CustomUser, ProductRequest, Profile, Relationship, Post, BankAccount, ProductRequestStatus, Transport
)
from .forms import (
    BankAccountForm, ContactForm, ProductRequestForm, SignUpForm, PostForm, TransportForm
)

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


'''
---------------
Vista principal
---------------
'''
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


'''
-------------------------
Vista de inicio de sesion
-------------------------
'''
def login(request):
    return render(request, 'login.html')


'''
--------------------------
Vista de perfil de usuario
--------------------------
'''
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


'''
--------------------------------
Vista de publicacion de producto
--------------------------------
'''
@login_required
def post_product(request):
	current_user = get_object_or_404(CustomUser, pk=request.user.pk)
	if request.method == 'POST':
		form = PostForm(request.POST, request.FILES)#eliminar request.FILES si hay problema
		if form.is_valid():
			post = form.save(commit=False)
			post.user = current_user
			post.save()
			return redirect('feed')
	else:
		form = PostForm()
	return render(request, 'post-product.html', {'form' : form })


'''
----------------------------------
Vista de publicacion de transporte
----------------------------------
'''
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


'''
---------------------------
Vista de la cuenta bancaria
---------------------------
'''
@login_required
def bank_account(request):
	#current_user = request.user
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

	return render(
		request, 'bank.html',
		{
			'user' : user,
			'banks' : banks,
			'form' : form,
		}
	)


'''
------------------------------------------
Vista de la eliminacion de cuenta bancaria
------------------------------------------
'''
@login_required
def delete_bank_account(request, id_bank_account = None):
	bank = BankAccount.objects.filter(pk=id_bank_account)
	bank.delete()
	return redirect('bank')


'''
------------------------------
Vista de solicitud de producto
------------------------------
'''
@login_required
def product_request(request):
	current_user = get_object_or_404(CustomUser, pk=request.user.pk)
	if request.method == 'POST':
		form = ProductRequestForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.user = current_user
			post.save()
			return redirect('feed')
	else:
		form = ProductRequestForm()
	return render(request, 'product-request.html', {'form' : form })


'''
------------------------------------
Vista de las solicitudes de producto
------------------------------------
'''
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


'''
---------------------------------------------------
Vista del estado de solicitud por parte del cliente
---------------------------------------------------
'''
@login_required
def client_request_status(request, id_offered_product):
	print(id_offered_product)

	requests = ProductRequestStatus.objects.filter(pk = id_offered_product)
	#requests = ProductRequestStatus.objects.all()
	print(requests)

	return render(request, 'request-status.html', {'requests' : requests})


'''
----------------------------------------------------------------
Vista del proceso de venta de los productos ofrecidos
----------------------------------------------------------------
'''
@login_required
def decline_product_offer(request, id_offered_product = None):

	status = 'RECHAZADO'

	product_offer = ProductRequestStatus.objects.get(pk = id_offered_product)
	product_offer.status = status
	product_offer.save()

	return redirect('request')

@login_required
def accept_product_offer(request, id_offered_product = None):
	status = 'APROBADO'

	product_offer = ProductRequestStatus.objects.get(pk = id_offered_product)
	product_offer.status = status
	product_offer.save()

	return redirect('request')

@login_required
def delete_product_offer(request, id_offered_product = None):

	product_offer = ProductRequestStatus.objects.filter(pk = id_offered_product)
	product_offer.delete()

	return redirect('request')


'''
--------------------------------
Vista de los productos ofrecidos
--------------------------------
'''
@login_required
def offer_product(request, id_offered_product = None):
	status = 'PENDIENTE'

	name_offered_product = request.user.posts.get(id = id_offered_product)

	product = ProductRequestStatus(
		id_offered_product = id_offered_product,
		offer = str(name_offered_product),
		status = str(status)
	)
	product.save()

	return redirect('request')

'''
----------------------------------------------------------------
Vista de los transportes publicados por el usuario Transportista
----------------------------------------------------------------
'''
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


'''
-----------------------------------------------
Vista de las publicaciones del producto creadas
-----------------------------------------------
'''
@login_required
def feed(request):
	posts = Post.objects.all()

	context = { 'posts': posts}
	return render(request, 'feed.html', context)


'''
----------------------------
Vista de registro de usuario
----------------------------
'''
def register(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)

		if form.is_valid():
			form.save()

			return redirect('home')
	else:
		form = SignUpForm()

	context = { 'form' : form }
	return render(request, 'register.html', context)


'''
-------------------------------------
Vista del inicio de sesion de usuario
-------------------------------------
'''
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


'''
----------------------------------------------------------------
Vista de las relaciones que pueden tener los usuarios
----------------------------------------------------------------
'''
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



'''
--------
API REST
--------
'''
from rest_framework import viewsets

from .serializers import (
	CustomUserSerializer, ProductRequestSerializer, ProfileSerializer,
	PostSerializer, BankAccountSerializer, ProductRequestStatusSerializer, TransportSerializer
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

class PostViewSet(viewsets.ModelViewSet):
	queryset = Post.objects.all()
	serializer_class = PostSerializer

class BankAccountViewSet(viewsets.ModelViewSet):
	queryset = BankAccount.objects.all()
	serializer_class = BankAccountSerializer

class ProductRequestStatusViewSet(viewsets.ModelViewSet):
	queryset = ProductRequestStatus.objects.all()
	serializer_class = ProductRequestStatusSerializer

class TransportViewSet(viewsets.ModelViewSet):
	queryset = Transport.objects.all()
	serializer_class = TransportSerializer