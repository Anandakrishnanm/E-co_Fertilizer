# from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

# Custom User Model
class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_buyer = models.BooleanField(default=False)

    # Fix conflicts with Django's default auth system
    groups = models.ManyToManyField(Group, related_name="store_users", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="store_users_permissions", blank=True)

    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.username


# Product Model
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="products/")
    category = models.CharField(max_length=100, choices=[('Fertilizer', 'Fertilizer'), ('Pesticide', 'Pesticide')])
    
    def __str__(self):
        return self.name

# Cart Model
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.product.price * self.quantity  # Calculate total dynamically

    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.quantity})"

    


class Order(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Shipped", "Shipped"),
        ("Delivered", "Delivered"),
        ("Cancelled", "Cancelled"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    date_ordered = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")

    # Set default values to avoid migration issues
    full_name = models.CharField(max_length=255, default="Unknown Buyer")
    address = models.TextField(default="Unknown Address")
    phone = models.CharField(max_length=15, default="0000000000")

    def total_price(self):
        return self.quantity * self.product.price

    def __str__(self):
        return f"Order {self.id} - {self.product.name} - {self.user.username}"


