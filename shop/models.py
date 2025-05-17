from django.db import models
from django.contrib.auth import get_user_model
from cloudinary.models import CloudinaryField

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
