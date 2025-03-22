from django.urls import path
from .views import list_view

urlpatterns = [
    path("products/", list_view, name="products__list_view"),
]
