# API REST


from rest_framework import viewsets

from .models import (
    CustomUser,
	ProductRequest,
	Profile,
	Relationship,
	Product,
	BankAccount,
	ProductRequestStatus,
	Transport,
	TransportRequestStatus,
	Transaction
)

from .serializers import (
	CustomUserSerializer,
	ProductRequestSerializer,
	ProfileSerializer,
	ProductSerializer,
	BankAccountSerializer,
	ProductRequestStatusSerializer,
	TransportSerializer,
	TransportRequestStatusSerializer,
    TransactionSerializer
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

class TransportRequestStatusViewSet(viewsets.ModelViewSet):
	queryset = TransportRequestStatus.objects.all()
	serializer_class = TransportRequestStatusSerializer

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer