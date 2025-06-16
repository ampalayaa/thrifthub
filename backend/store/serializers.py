from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Product, Category, Order, OrderItem, Wishlist

# --- Category ---
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


# --- Product ---
class ProductSerializer(serializers.ModelSerializer):
    seller_username = serializers.CharField(source='seller.username', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'seller',            # user ID
            'seller_username',   # readable name
            'name',
            'description',
            'price',
            'category',
            'category_name',
            'condition',
            'image',
            'is_available',
            'created_at',
        ]
        read_only_fields = ['seller', 'created_at']


# --- Order Item ---
class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'quantity']


# --- Order ---
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    buyer_username = serializers.CharField(source='buyer.username', read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'buyer', 'buyer_username', 'created_at', 'is_paid', 'total_price', 'items']
        read_only_fields = ['buyer', 'created_at']


# --- Wishlist ---
class WishlistSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_image = serializers.ImageField(source='product.image', read_only=True)

    class Meta:
        model = Wishlist
        fields = ['id', 'product', 'product_name', 'product_image', 'added_at']
