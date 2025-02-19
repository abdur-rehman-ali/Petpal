from django.contrib import admin
from .models import Pet


@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ("name", "pet_type", "breed", "price", "status")
    list_filter = ("pet_type", "status")
    search_fields = ("name", "breed")
