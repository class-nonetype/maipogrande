from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView

from rest_framework import routers









router = routers.DefaultRouter()

router.register(r'custom-user', views.CustomUserViewSet)
router.register(r'product-request', views.ProductRequestViewSet)
router.register(r'profile', views.ProfileViewSet)
router.register(r'post', views.PostViewSet)
router.register(r'bank-account', views.BankAccountViewSet)
router.register(r'product-request-status', views.ProductRequestStatusViewSet)
router.register(r'transport', views.TransportViewSet)


urlpatterns = [

	# Vista principal
	path('', views.home, name='home'),

	# Vista de publicaciones
	path('feed/', views.feed, name='feed'),

	# Vista del perfil de usuario
	path('profile/<str:username>/', views.profile, name='profile'),

	# Vista de registro de usuario
	path('register/', views.register, name='register'),

	# Vista de inicio de sesion
	path('login/', LoginView.as_view(template_name='login.html'), name='login'),

	# Vista de cierre de sesion
	path('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),

	# Vista de publicaciones
	path('post/product/', views.post_product, name='post_product'),
	path('post/transport/', views.post_transport, name='post_transport'),

	# Vista de banco
	path('bank/', views.bank_account, name='bank'),
	path('bank/delete/<int:id_bank_account>/', views.delete_bank_account, name='delete_bank_account'),

	# Interes del usuario
	path('follow/<str:username>/', views.follow, name='follow'),
	path('unfollow/<str:username>/', views.unfollow, name='unfollow'),

	# Vista de solicitud de producto
	path('product/request/', views.product_request, name='product_request'),

	# Vista de solicitudes de producto
	path('request/', views.client_request, name='request'),

	# Vista de transportes del usuario
	path('transport/', views.transport, name ='transport'),
	
	# Vista del estado de solicitud del producto
	path('request/status/<int:id_offered_product>/', views.client_request_status, name = 'client_request_status'),
	path('request/status/decline/<int:id_offered_product>/', views.decline_product_offer, name='decline_product_offer'),
	path('request/status/accept/<int:id_offered_product>/', views.accept_product_offer, name='accept_product_offer'),
	path('request/status/delete/<int:id_offered_product>/', views.delete_product_offer, name='delete_product_offer'),
	
	# Vista de producto ofrecido
	path('request/offer/product/<int:id_offered_product>/', views.offer_product, name='offer_product'),

	# Vista de API REST
	path('api/', include(router.urls), name = 'apirest'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

