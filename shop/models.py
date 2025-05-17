from django.db import models
from django.contrib.auth import get_user_model
from cloudinary.models import CloudinaryField
from decimal import Decimal

User = get_user_model()


class Product(models.Model):
    PET_CATEGORY_CHOICES = (
        ("DOG", "Dog"),
        ("CAT", "Cat"),
        ("BIRD", "Bird"),
        ("FISH", "Fish"),
        ("REPTILE", "Reptile"),
        ("SMALL_ANIMAL", "Small Animal"),
        ("OTHER", "Other"),
    )

    PRODUCT_TYPE_CHOICES = (
        ("FOOD", "Food"),
        ("TOY", "Toy"),
        ("ACCESSORY", "Accessory"),
        ("HEALTH", "Health Care"),
        ("GROOMING", "Grooming"),
        ("OTHER", "Other"),
    )

    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField(default=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="products")
    image = CloudinaryField("image", blank=True, null=True)
    pet_category = models.CharField(
        max_length=20, choices=PET_CATEGORY_CHOICES, default="OTHER"
    )
    product_type = models.CharField(
        max_length=20, choices=PRODUCT_TYPE_CHOICES, default="OTHER"
    )

    def __str__(self):
        return f"{self.name} ({self.get_pet_category_display()})"

    class Meta:
        ordering = ["-created_at"]


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())

    def __str__(self):
        return f"Cart of {self.user.username}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"


class Order(models.Model):
    STATUS_CHOICES = (
        ("PENDING", "Pending"),
        ("PROCESSING", "Processing"),
        ("SHIPPED", "Shipped"),
        ("DELIVERED", "Delivered"),
        ("CANCELLED", "Cancelled"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal("0.00")
    )

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def total_price(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product.name} @ {self.price}"
