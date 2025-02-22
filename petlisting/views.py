from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Pet


# Create your views here.
def list_view(request):
    pets = Pet.objects.all().order_by("-created_at")
    paginator = Paginator(pets, 10)
    page_number = request.GET.get("page")
    page_object = paginator.get_page(page_number)
    template_name = "petlisting/listing.html"
    context = {"pets": page_object}
    return render(request, template_name, context=context)
