from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username']

class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class ProductImageSerializer(ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'

class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class ProductSerializerImage(ModelSerializer):
    images = ProductImageSerializer(many = True, read_only = True)
    class Meta:
        model = Product
        fields = ['title', 'body', 'id', 'author', 'price', 'quantity', 'banner', 'images']

class CartSerializer(ModelSerializer):
    class Meta:
        model = Cart
        fields = "__all__"

class CartProductSerializer(ModelSerializer):
    class Meta:
        depth = 1
        model = CartProduct
        fields = "__all__"

class CartSerializerGet(ModelSerializer):
    cart_products = CartProductSerializer(many = True, read_only = True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields =['id', 'user', 'total_price', 'cart_products']
    
    def get_total_price(self, obj):
        return obj.total_price

class OrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

