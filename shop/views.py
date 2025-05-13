from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Product


def list_view(request):
    products_list = Product.objects.all().order_by("-created_at")

    paginator = Paginator(products_list, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "products": page_obj,
    }
    template_name = "shop/products_listing.html"
    return render(request, template_name, context)
