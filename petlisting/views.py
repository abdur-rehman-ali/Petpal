from django.shortcuts import render
from .models import Pet


# Create your views here.
def list_view(request):
    pets = Pet.objects.all()
    template_name = "petlisting/listing.html"
    context = {"pets": pets}
    return render(request, template_name, context=context)
