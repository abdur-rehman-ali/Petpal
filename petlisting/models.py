from django.db import models
from django.contrib.auth import get_user_model
from cloudinary.models import CloudinaryField

User = get_user_model()


class Pet(models.Model):
    PET_TYPES = [
        ("dog", "Dog"),
        ("cat", "Cat"),
        ("bird", "Bird"),
        ("fish", "Fish"),
        ("other", "Other"),
    ]

    GENDER_CHOICES = [("male", "Male"), ("female", "Female")]

    STATUS_CHOICES = [("available", "Available"), ("sold", "Sold")]

    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="pets")
    name = models.CharField(max_length=100)
    pet_type = models.CharField(max_length=10, choices=PET_TYPES)
    breed = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    location = models.CharField(max_length=100)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="available",
    )
    image = CloudinaryField("image", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
