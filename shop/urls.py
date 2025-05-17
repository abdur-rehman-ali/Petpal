from django.urls import path
from .views import (
    list_view,
    create_view,
    detail_view,
    edit_view,
    delete_view,
    add_to_cart,
    remove_from_cart,
    update_cart_item,
    view_cart,
    checkout,
    place_order,
    order_detail,
)

urlpatterns = [
    path("products/", list_view, name="products__list_view"),
    path("products/create/", create_view, name="products__create_view"),
    path("products/<int:product_id>/", detail_view, name="product__detail_view"),
    path("products/<int:product_id>/edit", edit_view, name="product__edit_view"),
    path("products/<int:product_id>/delete", delete_view, name="product__delete_view"),
    path("cart/add/<int:product_id>/", add_to_cart, name="add_to_cart"),
    path("cart/remove/<int:cart_item_id>/", remove_from_cart, name="remove_from_cart"),
    path("cart/update/<int:cart_item_id>/", update_cart_item, name="update_cart_item"),
    path("cart/", view_cart, name="view_cart"),
    path("checkout/", checkout, name="checkout"),
    path("checkout/place-order/", place_order, name="place_order"),
    path("orders/<int:order_id>/", order_detail, name="order_detail"),
]
