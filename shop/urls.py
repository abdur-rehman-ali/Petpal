from django.urls import path
from .views import list_view, create_view

urlpatterns = [
    path("products/", list_view, name="products__list_view"),
    path("products/create/", create_view, name="products__create_view"),
]
