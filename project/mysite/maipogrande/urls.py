from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView

from rest_framework import routers









router = routers.DefaultRouter()

router.register(r'CustomUser', views.CustomUserViewSet)
router.register(r'ProductRequest', views.ProductRequestViewSet)
router.register(r'Profile', views.ProfileViewSet)
router.register(r'Post', views.PostViewSet)
router.register(r'BankAccount', views.BankAccountViewSet)
router.register(r'ProductRequestStatus', views.ProductRequestStatusViewSet)


urlpatterns = [
	path('', views.home, name='home'),
	path('feed/', views.feed, name='feed'),
	path('profile/<str:username>/', views.profile, name='profile'),
	path('register/', views.register, name='register'),
	path('login/', LoginView.as_view(template_name='login.html'), name='login'),
	path('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),
	path('post/', views.post, name='post'),
	path('bank/', views.bank_account, name='bank'),
	path('bank/delete/<int:id_bank_account>/', views.delete_bank_account, name='delete_bank_account'),

	# Interes del usuario
	path('follow/<str:username>/', views.follow, name='follow'),
	path('unfollow/<str:username>/', views.unfollow, name='unfollow'),

	# Solicitud de producto
	path('product/request/', views.product_request, name='product_request'),

	# Solicitudes
	path('request/', views.client_request, name='request'),
	
	# <Cliente>	  -> Estado de la solicitud
	path('request/status/<int:id_offered_product>/', views.client_request_status, name = 'client_request_status'),
	
	# <Productor> -> Ofrecer producto
	path('request/offer/product/<int:id_offered_product>/', views.offer_product, name='offer_product'),

	# <API>		  -> Productor de datos
	path('api/', include(router.urls), name = 'apirest'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

