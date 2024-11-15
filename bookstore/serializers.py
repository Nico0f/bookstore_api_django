# bookstore/serializers.py
from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'phone', 'avatar', 
                 'role', 'is_active', 'date_joined', 'last_login')
        read_only_fields = ('date_joined', 'last_login')

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

class ShoppingCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingCart
        fields = '__all__'

class ShoppingOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingOrder
        fields = '__all__'

class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = '__all__'

class CheckoutOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckoutOrder
        fields = '__all__'

class NewsletterListSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsletterList
        fields = '__all__'