from django.shortcuts import get_object_or_404, render, redirect
from django.core.paginator import Paginator
from .models import Product
from .filters import ProductFilter
from .forms import ProductForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages


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


def detail_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    template_name = "shop/detail_view.html"
    context = {"product": product}
    return render(request, template_name, context=context)


@login_required
def create_view(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            messages.success(request, f"{product.name} has been created successfully!")
            return redirect("product__detail_view", product_id=product.id)
    else:
        form = ProductForm()

    template_name = "shop/create_edit_view_template.html"
    context = {"form": form, "is_edit": False}
    return render(request, template_name, context=context)


@login_required
def edit_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f"{product.name} has been updated successfully!")
            return redirect("product__detail_view", product_id=product.id)
    else:
        form = ProductForm(instance=product)

    template_name = "shop/create_edit_view_template.html"
    context = {"form": form, "product": product, "is_edit": True}
    return render(request, template_name, context)


@login_required
def delete_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == "POST":
        product.delete()
        messages.success(request, f"{product.name} has been deleted successfully.")
        return redirect("products__list_view")
    template_name = "shop/product_confirm_delete.html"
    context = {"product": product}
    return render(request, template_name, context)
