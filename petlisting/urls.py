from django.urls import path
from .views import list_view, detail_view, create_view, edit_view, delete_view

urlpatterns = [
    path("pets/", list_view, name="petlisting__list_view"),
    path("pets/<int:pet_id>/", detail_view, name="petlisting__detail_view"),
    path("pets/create/", create_view, name="petlisting__create_view"),
    path("pets/<int:pet_id>/edit", edit_view, name="petlisting__edit_view"),
    path("pets/<int:pet_id>/delete", delete_view, name="petlisting__delete_view"),
]
