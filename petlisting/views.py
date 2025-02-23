from django.shortcuts import get_object_or_404, render, redirect
from django.core.paginator import Paginator
from .models import Pet
from .filters import PetFilter
from .forms import PetForm


# Create your views here.
def list_view(request):
    # Qeury pets_list lists
    pets_list = Pet.objects.all().order_by("-created_at")
    # Apply filters
    pet_filters = PetFilter(request.GET, queryset=pets_list)
    pets_list = pet_filters.qs
    # Apply pagination
    paginator = Paginator(pets_list, 12)
    page_number = request.GET.get("page")
    page_object = paginator.get_page(page_number)
    # Render template
    template_name = "petlisting/listing.html"
    context = {"pets": page_object, "filters": pet_filters}
    return render(request, template_name, context=context)


def detail_view(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    template_name = "petlisting/detail_view.html"
    context = {"pet": pet}
    return render(request, template_name, context=context)


def create_view(request):
    if request.method == "POST":
        form = PetForm(request.POST)
        if form.is_valid():
            pet = form.save(commit=False)
            pet.seller = request.user
            pet.save()
            return redirect("petlisting__detail_view", pet_id=pet.id)
    else:
        form = PetForm()

    template_name = "petlisting/create_edit_view_template.html"
    context = {"form": form, "is_edit": False}
    return render(request, template_name, context=context)


def edit_view(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    if request.method == "POST":
        form = PetForm(request.POST, instance=pet)
        if form.is_valid():
            form.save()
            return redirect("petlisting__detail_view", pet_id=pet.id)
    else:
        form = PetForm(instance=pet)

    template_name = "petlisting/create_edit_view_template.html"
    context = {"form": form, "pet": pet, "is_edit": True}
    return render(request, template_name, context)
