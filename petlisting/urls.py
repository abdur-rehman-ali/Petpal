from django.urls import path
from .views import list_view, detail_view

urlpatterns = [
    path("pets/", list_view, name="petlisting__list_view"),
    path("pets/<int:pet_id>/", detail_view, name="petlisting__detail_view"),
]
