from django.contrib.auth import authenticate, login

from django.shortcuts import render, redirect, get_object_or_404

from .models import (
    CustomUser, ProductRequest, Profile, Relationship, Post, BankAccount, ProductRequestStatus
)
from .forms import (
    BankAccountForm, ContactForm, ProductRequestForm, SignUpForm, PostForm
)

from django.contrib import messages
from django.contrib.auth.decorators import login_required


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

def login(request):
    return render(request, 'login.html')

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

@login_required
def post(request):
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
	return render(request, 'post.html', {'form' : form })

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


@login_required
def delete_bank_account(request, id_bank_account = None):
	bank = BankAccount.objects.filter(pk=id_bank_account)
	bank.delete()
	return redirect('bank')

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

@login_required
def client_request(request):

	current_user = request.user

	if current_user.type == 'PRODUCTOR':

		requests = ProductRequest.objects.all()
		posts = current_user.posts.all()
	
	
	elif current_user.type == 'CLIENTE EXTERNO' or current_user.type == 'CLIENTE INTERNO':
		#requests = current_user.posts.all()
		requests = ProductRequest.objects.filter(user = current_user.id)
		posts = current_user
	
	else:
		pass

	return render(request, 'request.html', {'posts' : posts, 'requests' : requests})

@login_required
def client_request_status(request, id_offered_product):
	requests = ProductRequestStatus.objects.filter(id_offered_product = id_offered_product)

	return render(request, 'request-status.html', {'requests' : requests})



@login_required
def offer_product(request, id_offered_product = None):
	status = 'PENDIENTE'

	name_offered_product = request.user.posts.get(id = id_offered_product)

	product = ProductRequestStatus(
		id_offered_product = id_offered_product,
		offer = name_offered_product,
		status = status
	)
	product.save()

	return redirect('request')

def feed(request):
	posts = Post.objects.all()

	context = { 'posts': posts}
	return render(request, 'feed.html', context)

def register(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)

		if form.is_valid():
			form.save()

			return redirect('feed')
	else:
		form = SignUpForm()

	context = { 'form' : form }
	return render(request, 'register.html', context)



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




from rest_framework import viewsets

from .serializers import (
	CustomUserSerializer, ProductRequestSerializer, ProfileSerializer,
	PostSerializer, BankAccountSerializer, ProductRequestStatusSerializer
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
	serializer_class = ProductRequestStatus