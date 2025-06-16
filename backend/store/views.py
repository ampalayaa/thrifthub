from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Product, Category, Order, OrderItem, Wishlist
from .serializers import (
    ProductSerializer,
    CategorySerializer,
    OrderSerializer,
    WishlistSerializer,
)
from rest_framework.views import APIView


# -------- CATEGORY --------
class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# -------- PRODUCT --------
class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.filter(is_available=True).order_by('-created_at')
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        if self.request.user != serializer.instance.seller:
            raise PermissionDenied("You can only update your own product.")
        serializer.save()

    def perform_destroy(self, instance):
        if self.request.user != instance.seller:
            raise PermissionDenied("You can only delete your own product.")
        instance.delete()


# -------- ORDER --------
class OrderListCreateView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(buyer=self.request.user)

    def perform_create(self, serializer):
        serializer.save(buyer=self.request.user)


# -------- WISHLIST --------
class WishlistView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        wishlist = Wishlist.objects.filter(user=request.user)
        serializer = WishlistSerializer(wishlist, many=True)
        return Response(serializer.data)

    def post(self, request):
        product_id = request.data.get('product_id')
        product = get_object_or_404(Product, id=product_id)
        wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)
        if not created:
            return Response({'message': 'Already in wishlist'}, status=status.HTTP_200_OK)
        return Response({'message': 'Added to wishlist'}, status=status.HTTP_201_CREATED)

    def delete(self, request):
        product_id = request.data.get('product_id')
        Wishlist.objects.filter(user=request.user, product__id=product_id).delete()
        return Response({'message': 'Removed from wishlist'}, status=status.HTTP_204_NO_CONTENT)
