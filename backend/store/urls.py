from django.urls import path
from . import views

urlpatterns = [
    # Category
    path('categories/', views.CategoryListView.as_view(), name='category-list'),

    # Products
    path('products/', views.ProductListCreateView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),

    # Orders
    path('orders/', views.OrderListCreateView.as_view(), name='order-list-create'),

    # Wishlist
    path('wishlist/', views.WishlistView.as_view(), name='wishlist'),
]
