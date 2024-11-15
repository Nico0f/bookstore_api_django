from django.shortcuts import render
from rest_framework import viewsets, status, filters
from .models import *
from .serializers import *
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django.db.models import Avg, Count, Q
from django.utils import timezone
from datetime import datetime, timedelta
from django_filters.rest_framework import DjangoFilterBackend

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """Get current user's profile"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def toggle_active(self, request, pk=None):
        """Toggle user active status (admin only)"""
        user = self.get_object()
        user.is_active = not user.is_active
        user.save()
        return Response({'status': 'user status updated'})

    @action(detail=True, methods=['get'])
    def order_history(self, request, pk=None):
        """Get user's order history"""
        user = self.get_object()
        orders = ShoppingOrder.objects.filter(user=user)
        serializer = ShoppingOrderSerializer(orders, many=True)
        return Response(serializer.data)

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['type', 'publisher', 'best_seller', 'on_offer']
    search_fields = ['title', 'description', 'isbn13']
    ordering_fields = ['rating', 'price_hardcover', 'published_date']
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAdminUser()]

    @action(detail=False, methods=['get'])
    def bestsellers(self, request):
        """Get bestselling books"""
        bestsellers = self.queryset.filter(best_seller=True)
        serializer = self.get_serializer(bestsellers, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def on_sale(self, request):
        """Get books currently on sale"""
        on_sale = self.queryset.filter(on_offer=True)
        serializer = self.get_serializer(on_sale, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def similar_books(self, request, pk=None):
        """Get similar books based on genres"""
        book = self.get_object()
        genres = book.BookGenre_set.values_list('genre', flat=True)
        similar_books = Book.objects.filter(
            BookGenre__genre__in=genres
        ).exclude(id=book.id).distinct()[:5]
        serializer = self.get_serializer(similar_books, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def top_rated(self, request):
        """Get top rated books"""
        top_books = self.queryset.filter(
            rating__gte=4.0,
            amountRatings__gte=100
        ).order_by('-rating')[:10]
        serializer = self.get_serializer(top_books, many=True)
        return Response(serializer.data)

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    @action(detail=True, methods=['get'])
    def books(self, request, pk=None):
        """Get all books by this author"""
        author = self.get_object()
        books = Book.objects.filter(author__author=author)
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def statistics(self, request, pk=None):
        """Get author statistics"""
        author = self.get_object()
        books = Book.objects.filter(author__author=author)
        stats = {
            'total_books': books.count(),
            'average_rating': books.aggregate(Avg('rating'))['rating__avg'],
            'total_ratings': books.aggregate(Count('amountRatings'))['amountRatings__count'],
            'bestsellers': books.filter(best_seller=True).count()
        }
        return Response(stats)

class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

    @action(detail=True, methods=['get'])
    def books(self, request, pk=None):
        """Get all books in this genre"""
        genre = self.get_object()
        books = Book.objects.filter(BookGenre__genre=genre)
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def popular_authors(self, request, pk=None):
        """Get popular authors in this genre"""
        genre = self.get_object()
        authors = Author.objects.filter(
            book__BookGenre__genre=genre
        ).annotate(
            book_count=Count('book'),
            avg_rating=Avg('book__rating')
        ).order_by('-book_count')[:5]
        return Response([{
            'name': author.name,
            'books': author.book_count,
            'average_rating': author.avg_rating
        } for author in authors])

class ShoppingCartViewSet(viewsets.ModelViewSet):
    queryset = ShoppingCart.objects.all()
    serializer_class = ShoppingCartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ShoppingCart.objects.filter(user=self.request.user)

    @action(detail=True, methods=['post'])
    def add_item(self, request, pk=None):
        """Add item to cart"""
        cart = self.get_object()
        book_id = request.data.get('book_id')
        try:
            book = Book.objects.get(id=book_id)
            CartProduct.objects.create(cart=cart, book=book)
            return Response({'status': 'item added to cart'})
        except Book.DoesNotExist:
            return Response({'error': 'book not found'}, status=400)

    @action(detail=True, methods=['post'])
    def remove_item(self, request, pk=None):
        """Remove item from cart"""
        cart = self.get_object()
        book_id = request.data.get('book_id')
        CartProduct.objects.filter(cart=cart, book_id=book_id).delete()
        return Response({'status': 'item removed from cart'})

    @action(detail=True, methods=['get'])
    def total(self, request, pk=None):
        """Calculate cart total"""
        cart = self.get_object()
        total = sum(
            product.book.price_hardcover 
            for product in cart.cartProducts.all()
        )
        return Response({'total': total})
    
class ShoppingOrderViewSet(viewsets.ModelViewSet):
    queryset = ShoppingOrder.objects.all()
    serializer_class = ShoppingOrderSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['orderStatus']

    def get_queryset(self):
        if self.request.user.is_staff:
            return ShoppingOrder.objects.all()
        return ShoppingOrder.objects.filter(user=self.request.user)

    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        """Update order status (admin only)"""
        order = self.get_object()
        new_status = request.data.get('status')
        if new_status:
            order.orderStatus = new_status
            order.save()
            return Response({'status': 'order status updated'})
        return Response({'error': 'no status provided'}, status=400)

    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        """Get order statistics (admin only)"""
        if not request.user.is_staff:
            return Response({'error': 'unauthorized'}, status=403)
            
        today = timezone.now()
        thirty_days_ago = today - timedelta(days=30)
        
        stats = {
            'total_orders': self.queryset.count(),
            'recent_orders': self.queryset.filter(
                createdAt__gte=thirty_days_ago
            ).count(),
            'status_breakdown': self.queryset.values('orderStatus').annotate(
                count=Count('id')
            ),
            'daily_orders': self.queryset.filter(
                createdAt__gte=thirty_days_ago
            ).extra(
                select={'day': 'date(created_at)'}
            ).values('day').annotate(count=Count('id')).order_by('day')
        }
        return Response(stats)

class CheckoutOrderViewSet(viewsets.ModelViewSet):
    queryset = CheckoutOrder.objects.all()
    serializer_class = CheckoutOrderSerializer

class NewsletterListViewSet(viewsets.ModelViewSet):
    queryset = NewsletterList.objects.all()
    serializer_class = NewsletterListSerializer
    permission_classes = [AllowAny]

    @action(detail=False, methods=['post'])
    def subscribe(self, request):
        """Subscribe to newsletter"""
        email = request.data.get('email')
        if not email:
            return Response({'error': 'email required'}, status=400)
        
        try:
            NewsletterList.objects.create(email=email)
            return Response({'status': 'subscribed successfully'})
        except:
            return Response({'error': 'already subscribed'}, status=400)

    @action(detail=False, methods=['post'])
    def unsubscribe(self, request):
        """Unsubscribe from newsletter"""
        email = request.data.get('email')
        NewsletterList.objects.filter(email=email).delete()
        return Response({'status': 'unsubscribed successfully'})