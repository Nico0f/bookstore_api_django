from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    phone = models.CharField(max_length=20, null=True, blank=True)
    avatar = models.CharField(max_length=255, null=True, blank=True)
    ROLE_CHOICES = [
        ('USER', 'User'),
        ('STAFF', 'Staff'),
        ('ADMIN', 'Admin'),
    ]
    role = models.CharField(max_length=5, choices=ROLE_CHOICES, default='USER')
    is_active = models.BooleanField(default=True)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='bookstore_user_groups',
        blank=True,
        help_text='The groups this user belongs to.'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='bookstore_user_permissions',
        blank=True,
        help_text='Specific permissions for this user.'
    )

class Book(models.Model):
    title = models.CharField(max_length=255, unique=True)
    publisher = models.CharField(max_length=255)
    published_date = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    type = models.CharField(max_length=50)
    page_count = models.IntegerField()
    curated_review = models.TextField(null=True, blank=True)
    curated_review_date = models.CharField(max_length=50, null=True, blank=True)
    curated_review_author = models.CharField(max_length=255, null=True, blank=True)
    isbn13 = models.CharField(max_length=13)
    cover = models.CharField(max_length=255)
    rating = models.FloatField()
    amount_ratings = models.IntegerField()
    one_rating = models.IntegerField()
    two_rating = models.IntegerField()
    three_rating = models.IntegerField()
    four_rating = models.IntegerField()
    five_rating = models.IntegerField()
    price_hardcover = models.DecimalField(max_digits=10, decimal_places=2)
    price_paperback = models.DecimalField(max_digits=10, decimal_places=2)
    price_ebook = models.DecimalField(max_digits=10, decimal_places=2)
    price_audiobook = models.DecimalField(max_digits=10, decimal_places=2)
    best_seller = models.BooleanField(default=False)
    ebook = models.BooleanField(default=True)
    audiobook = models.BooleanField(default=True)
    stock = models.IntegerField()
    on_offer = models.BooleanField(default=False)
    on_display = models.BooleanField(default=True)

class Author(models.Model):
    name = models.CharField(max_length=255, unique=True)
    about = models.TextField(null=True, blank=True)
    books = models.ManyToManyField(Book, through='BookAuthor')

class BookAuthor(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('author', 'book')

class Genre(models.Model):
    genre_name = models.CharField(max_length=255, unique=True)
    books = models.ManyToManyField(Book, through='BookGenre')

class BookGenre(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('genre', 'book')

class ShoppingCart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    books = models.ManyToManyField(Book, through='CartProduct')

class CartProduct(models.Model):
    cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('cart', 'book')

class ShippingAddress(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class UserAddress(models.Model):
    shipping_address = models.ForeignKey(ShippingAddress, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    address_number = models.CharField(max_length=50)
    details = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)

class ShoppingOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=255)
    email = models.EmailField()
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    shipping_method = models.CharField(max_length=100)
    shipping_amount = models.IntegerField()
    order_amount = models.IntegerField()
    taxes_amount = models.IntegerField()
    order_status = models.CharField(max_length=50)

class OrderProduct(models.Model):
    order = models.ForeignKey(ShoppingOrder, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    version = models.CharField(max_length=50)

class CheckoutOrder(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=255)
    email = models.EmailField()
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    shipping_method = models.CharField(max_length=100)
    items = models.JSONField()
    created_at = models.BigIntegerField()

class NewsletterList(models.Model):
    email = models.EmailField(unique=True)
