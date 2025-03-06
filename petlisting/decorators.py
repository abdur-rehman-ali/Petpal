from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Pet


def seller_required(view_func):
    """
    Custom decorator to ensure that only the seller of the pet can access the view.
    """

    @login_required
    def wrapper(request, *args, **kwargs):
        pet_id = kwargs.get("pet_id")
        pet = get_object_or_404(Pet, id=pet_id)

        if pet.seller != request.user:
            messages.error(request, "You do not have permission to access this page.")
            return redirect("petlisting__detail_view", pet_id=pet.id)
        return view_func(request, *args, **kwargs)

    return wrapper
