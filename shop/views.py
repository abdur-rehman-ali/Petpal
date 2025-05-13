from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Product
from .filters import ProductFilter


def list_view(request):
    # Get base queryset
    products_list = (
        Product.objects.select_related("seller").all().order_by("-created_at")
    )

    # Apply filters
    products_filter = ProductFilter(request.GET, queryset=products_list)
    products_list = products_filter.qs

    # Paginate results (12 items per page)
    paginator = Paginator(products_list, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "products": page_obj,
        "filters": products_filter,
        "total_products": products_list.count(),
    }
    return render(request, "shop/products_listing.html", context)
