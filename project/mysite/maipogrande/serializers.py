from rest_framework import serializers


from .models import (
    CustomUser,
    ProductRequest,
    Profile,
    Relationship,
    Product,
    BankAccount,
    ProductRequestStatus,
    Transport
)

# Serializador para la API

class CustomUserSerializer(serializers.ModelSerializer):
   class Meta:
       model = CustomUser
       fields = '__all__'


class ProductRequestSerializer(serializers.ModelSerializer):
   class Meta:
       model = ProductRequest
       fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
   class Meta:
       model = Profile
       fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
   class Meta:
       model = Product
       fields = '__all__'


class BankAccountSerializer(serializers.ModelSerializer):
   class Meta:
       model = BankAccount
       fields = '__all__'


class ProductRequestStatusSerializer(serializers.ModelSerializer):
   class Meta:
       model = ProductRequestStatus
       fields = '__all__'


class TransportSerializer(serializers.ModelSerializer):
   class Meta:
       model = Transport
       fields = '__all__'