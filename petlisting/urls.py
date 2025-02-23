from django.urls import path
from .views import list_view, detail_view, create_view

urlpatterns = [
    path("pets/", list_view, name="petlisting__list_view"),
    path("pets/<int:pet_id>/", detail_view, name="petlisting__detail_view"),
    path("pets/create/", create_view, name="petlisting__create_view"),
]
