from django.urls import path, include
from . import views

from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView

from rest_framework import routers


from .viewset import (
	CustomUserViewSet,
	ProductRequestViewSet,
	ProfileViewSet,
	ProductViewSet,
	BankAccountViewSet,
	ProductRequestStatusViewSet,
	TransportViewSet,
	TransactionViewSet,
	TransportRequestStatusViewSet,
	InternationalContractViewSet,
	ContractViewSet

)


###################################################################
#	Registro de las clases para la creacion de las url de API	  #
###################################################################

router = routers.DefaultRouter()

router.register(r'custom-user',CustomUserViewSet)
router.register(r'product-request', ProductRequestViewSet)
router.register(r'profile', ProfileViewSet)
router.register(r'post', ProductViewSet)
router.register(r'bank-account', BankAccountViewSet)
router.register(r'product-request-status', ProductRequestStatusViewSet)
router.register(r'transport', TransportViewSet)
router.register(r'transport-request-status', TransportRequestStatusViewSet)
router.register(r'transaction', TransactionViewSet)
router.register(r'contract', ContractViewSet)
router.register(r'international-contract', InternationalContractViewSet)


urlpatterns = [
	###################################################################
	#	URL principal												  #
	###################################################################
	path('', views.home, name = 'home'),

	###################################################################
	#	URL de publicaciones										  #
	###################################################################
	path('feed/', views.feed, name = 'feed'),

	###################################################################
	#	URL de busquedas											  #
	###################################################################
	path('search/product/', views.search_product, name = 'search_product'),
	path('search/product/purchased/', views.search_purchased_product, name = 'search_purchased_product'),
	path('search/request/status/', views.search_product_request, name = 'search_product_request'),

	###################################################################
	#	URL de perfiles												  #
	###################################################################
	path('profile/<str:username>/', views.profile, name='profile'),
	path('product/<int:id_product>/', views.view_product_post, name='view_product_post'),
	path('transport/<int:id_transport>/', views.view_transport_post, name='view_transport_post'),

	###################################################################
	#	URL de registro de usuario									  #
	###################################################################
	path('signup/', views.signup, name='signup'),

	###################################################################
	#	URL de inicio de sesion de usuario							  #
	###################################################################
	path('login/', LoginView.as_view(template_name = 'login.html'), name = 'login'),

	###################################################################
	#	URL de cierre de sesion\									  #
	###################################################################
	path('logout/', LogoutView.as_view(template_name = 'logout.html'), name = 'logout'),

	###################################################################
	#	URL de registro de publicaciones							  #
	###################################################################
	path('publish/product/post/', views.publish_product_post, name = 'publish_product_post'),
	path('publish/transport/post/', views.publish_transport_post, name = 'publish_transport_post'),
	path('publish/contract/', views.publish_contract, name = 'publish_contract'),


	path('contract/', views.contract, name = 'contract'),
	path('contract/generate/', views.generate_contract, name = 'generate_contract'),

	###################################################################
	#	URL de cuenta bancaria										  #
	###################################################################
	path('bank/account/', views.bank_account, name = 'bank_account'),
	path('bank/account/delete/<int:id_bank_account>/', views.delete_bank_account, name = 'delete_bank_account'),
	path('bank/account/modify/<int:id_bank_account>/', views.modify_bank_account, name = 'modify_bank_account'),

	###################################################################
	#	URL de interes de usuario									  #
	###################################################################
	path('follow/<str:username>/', views.follow, name = 'follow'),
	path('unfollow/<str:username>/', views.unfollow, name = 'unfollow'),

	###################################################################
	#	URL de solicitud de producto								  #
	###################################################################
	path('product/request/', views.product_request, name='product_request'),

	###################################################################
	#	URL de transaccion de producto								  #
	###################################################################
	path('product/transaction/', views.purchased_products, name = 'purchased_products'),

	###################################################################
	#	URL de transaccion de producto vendido						  #
	###################################################################
	path('product/<int:id_product>/sold/', views.product_sold, name = 'product_sold'),


	###################################################################
	#	URL de aceptar el producto ofrecido							  #
	path('client/request/status/accept/product/<int:id_product>/transaction/', views.accept_offered_product, name = 'accept_offered_product'),

	#	URL de rechazar el producto ofrecido						  #
	path('client/request/status/decline/product/<int:id_product>/', views.decline_offered_product, name='decline_offered_product'),

	#	URL de estado de solicitud del producto						  #
	###################################################################
	path('client/request/status/delete/<int:id_offered_product>/', views.delete_offered_product, name='delete_offered_product'),

	###################################################################
	#	URL de transaccion de venta									  #
	###################################################################
	path(
		'transaction/<int:id_bank_account>/<int:amount>/<int:id_product>/<int:quantity>/<int:id_producer>/<int:id_client>/<int:price>/<str:type_sale>',
		views.generate_sales_transaction, name = 'generate_sales_transaction'
	),

	path('transaction/product/<int:id_product>/', views.product_sale, name='product_sale'),








	###################################################################
	#	URL de estado de solicitud									  #
	###################################################################
	path('client/request/status/', views.client_request_status, name = 'client_request_status'),
	path('client/request/status/<int:id_product_request>/', views.client_requests_status, name = 'client_requests_status'),


	###################################################################
	#	URL de recarga de creditos virtuales						  #
	###################################################################
	path('recharge/<int:recharge_amount>/<int:id_bank>/', views.recharge_amount, name = 'recharge_amount'),
	path('recharge/', views.recharge, name = 'recharge'),




	###################################################################
	#	URL de orden												  #
	###################################################################
	path('product/<int:id_product>/transaction/<int:id_transaction>/', views.order_tracking, name='order_tracking'),
	path('product/<int:id_product>/transaction/<int:id_transaction>/change/status/0', views.switch_to_order_tracking_status_0, name = 'switch_to_order_tracking_status_0'),
	path('product/<int:id_product>/transaction/<int:id_transaction>/change/status/1', views.switch_to_order_tracking_status_1, name = 'switch_to_order_tracking_status_1'),
	path('product/<int:id_product>/transaction/<int:id_transaction>/change/status/2', views.switch_to_order_tracking_status_2, name = 'switch_to_order_tracking_status_2'),
	path('product/<int:id_product>/transaction/<int:id_transaction>/change/status/3', views.switch_to_order_tracking_status_3, name = 'switch_to_order_tracking_status_3'),


	###################################################################
	#	URL de solicitudes del cliente								  #
	###################################################################
	path('client/request/', views.client_request, name='client_request'),

	###################################################################
	#	URL de transportes del usuario								  #
	###################################################################
	path('transport/', views.transport, name ='transport'),


	###################################################################
	#	URL de envio de ofertas										  #
	###################################################################
	path('request/offer/product/<int:id_offered_product>/<int:id_product_request>/', views.offer_product, name='offer_product'),
	path('request/offer/transport/<int:id_transaction>/<int:id_product>/', views.offer_transport, name='offer_transport'),

	path('request/offer/transaction/<int:id_transaction>/<int:id_product>/<int:id_transport>/', views.transport_request, name = 'transport_request'),



	path('contract/activate/international/', views.international_contract_sales_process, name = 'international_contract_sales_process'),


	path('contract/international/', views.international_contract_process, name = 'international_contract_process'),
	path('contract/international/feed/', views.international_contract_feed, name = 'international_contract_feed'),
	path('contract/international/delete/<int:id_contract>/', views.delete_international_contract, name = 'delete_international_contract'),
	path('contract/international/renew/<int:id_contract>/', views.renew_international_contract, name = 'renew_international_contract'),
	path('contract/international/revoke/<int:id_contract>/', views.revoke_international_contract, name = 'revoke_international_contract'),



	path('product/total/', views.total_transactions_made, name = 'total_transactions'),
	###################################################################
	#	URL de API													  #
	###################################################################
	path('api/', include(router.urls), name = 'api'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

