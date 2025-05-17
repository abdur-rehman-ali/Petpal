from django.shortcuts import get_object_or_404, render, redirect
from django.core.paginator import Paginator
from .models import Product, Cart, CartItem, Order, OrderItem
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


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart, product=product, defaults={"quantity": 1}
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, f"{product.name} added to your cart.")
    return redirect("product__detail_view", product_id=product.id)


@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)
    cart_item.delete()
    messages.success(request, "Item removed from your cart.")
    return redirect("view_cart")


@login_required
def update_cart_item(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)
    quantity = int(request.POST.get("quantity", 1))

    if quantity > 0:
        cart_item.quantity = quantity
        cart_item.save()
        messages.success(request, "Cart updated.")
    else:
        cart_item.delete()
        messages.success(request, "Item removed from your cart.")

    return redirect("view_cart")


@login_required
def view_cart(request):
    cart = get_object_or_404(Cart, user=request.user)
    return render(request, "shop/cart.html", {"cart": cart})


@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)

    if not cart.items.exists():
        messages.warning(request, "Your cart is empty.")
        return redirect("view_cart")

    return render(request, "shop/checkout.html", {"cart": cart})


@login_required
def place_order(request):
    cart = get_object_or_404(Cart, user=request.user)

    if not cart.items.exists():
        messages.warning(request, "Your cart is empty.")
        return redirect("view_cart")

    # Create order
    order = Order.objects.create(user=request.user, total_price=cart.total_price)

    # Create order items
    for cart_item in cart.items.all():
        OrderItem.objects.create(
            order=order,
            product=cart_item.product,
            quantity=cart_item.quantity,
            price=cart_item.product.price,
        )

        # Update product stock
        cart_item.product.stock -= cart_item.quantity
        cart_item.product.save()

    # Clear the cart
    cart.items.all().delete()

    messages.success(request, "Your order has been placed successfully!")
    return redirect("order_detail", order_id=order.id)


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, "shop/order_detail.html", {"order": order})


@login_required
def my_orders(request):
    orders = (
        Order.objects.filter(items__product__seller=request.user)
        .distinct()
        .order_by("-created_at")
    )

    return render(request, "shop/my_orders.html", {"orders": orders})


@login_required
def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id, items__product__seller=request.user)

    if request.method == "POST":
        new_status = request.POST.get("status")
        if new_status in dict(Order.STATUS_CHOICES).keys():
            order.status = new_status
            order.save()
            messages.success(request, "Order status updated successfully!")
            return redirect("my_orders")
    return redirect("my_orders")
