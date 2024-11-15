from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff

class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or request.user.is_staff

# bookstore/filters.py
from django_filters import rest_framework as filters
from .models import Book, ShoppingOrder

class BookFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name="price_hardcover", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="price_hardcover", lookup_expr='lte')
    min_rating = filters.NumberFilter(field_name="rating", lookup_expr='gte')
    genre = filters.CharFilter(field_name='BookGenre__genre__genreName')
    author = filters.CharFilter(field_name='author__name')
    published_after = filters.DateFilter(field_name='publishedDate', lookup_expr='gte')
    published_before = filters.DateFilter(field_name='publishedDate', lookup_expr='lte')

    class Meta:
        model = Book
        fields = ['type', 'publisher', 'best_seller', 'on_offer', 'ebook', 'audiobook']

class OrderFilter(filters.FilterSet):
    min_amount = filters.NumberFilter(field_name="orderAmount", lookup_expr='gte')
    max_amount = filters.NumberFilter(field_name="orderAmount", lookup_expr='lte')
    created_after = filters.DateFilter(field_name='createdAt', lookup_expr='gte')
    created_before = filters.DateFilter(field_name='createdAt', lookup_expr='lte')

    class Meta:
        model = ShoppingOrder
        fields = ['orderStatus', 'shippingMethod']