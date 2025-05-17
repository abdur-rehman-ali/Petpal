from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "name",
            "description",
            "price",
            "stock",
            "is_available",
            "image",
            "pet_category",
            "product_type",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
        }
