from django.urls import path
from .views import list_view, create_view, detail_view, edit_view, delete_view

urlpatterns = [
    path("products/", list_view, name="products__list_view"),
    path("products/create/", create_view, name="products__create_view"),
    path("products/<int:product_id>/", detail_view, name="product__detail_view"),
    path("products/<int:product_id>/edit", edit_view, name="product__edit_view"),
    path("products/<int:product_id>/delete", delete_view, name="product__delete_view"),
]
