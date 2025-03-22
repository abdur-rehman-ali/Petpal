from django.shortcuts import render
from .models import Product


def list_view(request):
    products = Product.objects.all()
    context = {"products": products}
    template_name = "shop/products_listing.html"
    return render(request, template_name, context)
