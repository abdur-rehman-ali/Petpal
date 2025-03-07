from django.shortcuts import get_object_or_404, render, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Pet
from .filters import PetFilter
from .forms import PetForm
from .decorators import seller_required


def list_view(request):
    # Filter the pets
    [pets_filters, pets_list, total_pets] = filter_pets(request)

    # Apply pagination
    page_number = request.GET.get("page")
    page_object = paginate_queryset(pets_list, page_number)

    # Prepare context
    context = prepare_list_view_context(page_object, pets_filters, total_pets)

    # Render template
    template_name = "petlisting/listing.html"
    return render(request, template_name, context)


def detail_view(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    template_name = "petlisting/detail_view.html"
    context = {"pet": pet}
    return render(request, template_name, context=context)


@login_required
def create_view(request):
    if request.method == "POST":
        form = PetForm(request.POST)
        if form.is_valid():
            pet = form.save(commit=False)
            pet.seller = request.user
            pet.save()
            messages.success(request, f"{pet.name} has been created successfully!")
            return redirect("petlisting__detail_view", pet_id=pet.id)
    else:
        form = PetForm()

    template_name = "petlisting/create_edit_view_template.html"
    context = {"form": form, "is_edit": False}
    return render(request, template_name, context=context)


@seller_required
def edit_view(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    if request.method == "POST":
        form = PetForm(request.POST, instance=pet)
        if form.is_valid():
            form.save()
            messages.success(request, f"{pet.name} has been updated successfully!")
            return redirect("petlisting__detail_view", pet_id=pet.id)
    else:
        form = PetForm(instance=pet)

    template_name = "petlisting/create_edit_view_template.html"
    context = {"form": form, "pet": pet, "is_edit": True}
    return render(request, template_name, context)


@seller_required
def delete_view(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    if request.method == "POST":
        pet.delete()
        messages.success(request, f"{pet.name} has been deleted successfully.")
        return redirect("petlisting__list_view")
    template_name = "petlisting/pet_confirm_delete.html"
    context = {"pet": pet}
    return render(request, template_name, context)


# Private Methods
def filter_pets(request):
    pets_list = Pet.objects.select_related("seller").all().order_by("-created_at")
    pets_filters = PetFilter(request.GET, queryset=pets_list)
    pets_list = pets_filters.qs
    total_pets = pets_list.count()
    return [pets_filters, pets_list, total_pets]


def paginate_queryset(queryset, page_number, page_size=12):
    paginator = Paginator(queryset, page_size)
    page_object = paginator.get_page(page_number)
    return page_object


def prepare_list_view_context(page_object, pets_filters, total_pets):
    return {
        "pets": page_object,
        "filters": pets_filters,
        "total_pets": total_pets,
    }
