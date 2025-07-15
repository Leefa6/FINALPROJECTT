from django.db import models
from django.contrib.auth.models import User

# This file defines the database structure for the shop app.
# Each class represents a table in the database.

class Category(models.Model):
    """
    Represents a product category (e.g., Shirts, Shoes).
    Fields:
      - name: The display name of the category.
      - slug: A URL-friendly version of the name (used for filtering and clean URLs).
      - description: Optional text describing the category.
    """
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['name']  # Categories are ordered alphabetically by name.

    def __str__(self):
        return self.name

class Product(models.Model):
    """
    Represents a product for sale in the store.
    Fields:
      - name: The product's name.
      - slug: Used for clean URLs (e.g., /shop/product-slug/).
      - description: Details about the product.
      - price: The product's price.
      - image: An uploaded image of the product.
      - category: Links this product to a Category (many products can belong to one category).
    """
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True, null=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="products/")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # Many products to one category

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class Review(models.Model):
    """
    Stores a review left by a user for a product.
    Fields:
      - user: The user who wrote the review (linked to Django's User model).
      - product: The product being reviewed.
      - rating: Integer rating (1-5).
      - comment: The review text.
      - created_at: When the review was created.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']  # Newest reviews first

    def __str__(self):
        return f"Review by {str(self.user)} for {str(self.product)}"

class CartItem(models.Model):
    """
    (Not used in session-based cart, but kept for reference.)
    Represents an item in a user's cart (if using database cart).
    Fields:
      - user: The user who owns the cart item.
      - product: The product in the cart.
      - quantity: How many of this product.
      - added_at: When the item was added.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-added_at']

    def __str__(self):
        return f"{self.quantity} x {str(self.product)} for {str(self.user)}"

class Order(models.Model):
    """
    Represents a completed order placed by a user.
    Fields:
      - user: The user who placed the order.
      - items: The cart items included in the order (many-to-many relationship).
      - total: The total price of the order.
      - status: The order status (e.g., Pending, Shipped).
      - created_at: When the order was created.
    """
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Shipped", "Shipped"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(CartItem)  # An order can have many cart items
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.pk} by {str(self.user)}"
