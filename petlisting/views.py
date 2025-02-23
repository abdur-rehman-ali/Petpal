from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Pet
from .filters import PetFilter


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
