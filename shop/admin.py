from django.contrib import admin
from .models import Product


@admin.register(Product)
class PetAdmin(admin.ModelAdmin):
    list_display = ("name", "stock", "price", "is_available", "created_at")
    list_filter = ("name", "is_available")
